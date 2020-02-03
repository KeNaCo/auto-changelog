import logging
import re
from datetime import date
from hashlib import sha256
from typing import Any, Dict, List, Optional, Tuple

from auto_changelog.domain_model import Changelog, RepositoryInterface
from git import Commit, Repo, TagReference


class GitRepository(RepositoryInterface):
    def __init__(self, repository_path, *, latest_version: Optional[str] = None, skip_unreleased: bool = True):
        self.repository = Repo(repository_path, search_parent_directories=True)
        self.commit_tags_index = self._init_commit_tags_index(self.repository)
        # in case of defined latest version, unreleased is used as latest release
        self._skip_unreleased = skip_unreleased and not bool(latest_version)
        self._latest_version = latest_version or "Unreleased"

    def generate_changelog(
        self,
        title: str = "Changelog",
        description: str = "",
        remote: str = "origin",
        issue_pattern: Optional[str] = None,
        issue_url: Optional[str] = None,
        starting_commit: str = "",
        stopping_commit: str = "HEAD",
    ) -> Changelog:
        issue_url = issue_url or self._issue_from_git_remote_url(remote)
        changelog = Changelog(title, description, issue_pattern, issue_url)
        if self._repository_is_empty():
            logging.info("Repository is empty.")
            return changelog
        iter_rev = self._get_iter_rev(starting_commit, stopping_commit)
        commits = self.repository.iter_commits(iter_rev)
        # Some thoughts here
        #  First we need to check if all commits are "released". If not, we have to create our special "Unreleased"
        #  release. Then we simply iter over all commits, assign them to current release or create new if we find it.
        first_commit = True
        skip = self._skip_unreleased
        for commit in commits:
            if skip and commit not in self.commit_tags_index:
                continue
            else:
                skip = False

            if first_commit and commit not in self.commit_tags_index:
                changelog.add_release(self._latest_version, date.today(), sha256())
            first_commit = False

            if commit in self.commit_tags_index:
                attributes = self._extract_release_args(commit, self.commit_tags_index[commit])
                changelog.add_release(*attributes)

            attributes = self._extract_note_args(commit)
            changelog.add_note(*attributes)
        return changelog

    def _issue_from_git_remote_url(self, remote: str) -> Optional[str]:
        """ Creates issue url with {id} format key """
        try:
            url = self._remote_url(remote)
            return url + "/issues/{id}"
        except ValueError as e:
            logging.error("%s. Turning off issue links.", e)
            return None

    def _remote_url(self, remote: str) -> str:
        """ Extract remote url from remote url """
        url = self._get_git_url(remote=remote)
        # 'git@github.com:Michael-F-Bryan/auto-changelog.git' -> 'https://github.com/Michael-F-Bryan/auto-changelog'
        # 'https://github.com/Michael-F-Bryan/auto-changelog.git' -> 'https://github.com/Michael-F-Bryan/auto-changelog'
        url = re.sub(r"^(https|git|ssh)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$", r"https://\3/\4/\5", url)
        return url

    # This part is hard to mock, separate method is nice approach how to overcome this problem
    def _get_git_url(self, remote: str) -> str:
        remote_config = self.repository.remote(name=remote).config_reader
        # remote url can be in one of this three options
        # Test is the option exits before access it, otherwise the program crashes
        if remote_config.has_option("url"):
            return remote_config.get("url")
        elif remote_config.has_option("pushurl"):
            return remote_config.get("pushurl")
        elif remote_config.has_option("pullurl"):
            return remote_config.get("pullurl")
        else:
            return ""

    def _get_iter_rev(self, starting_commit: str, stopping_commit: str):
        if starting_commit:
            c = self.repository.commit(starting_commit)
            if not c.parents:
                # starting_commit is initial commit,
                # treat as default
                starting_commit = ""
            else:
                # iter_commits iters from the first rev to the second rev,
                # but not contains the second rev.
                # Here we set the second rev to its previous one then the
                # second rev would be included.
                starting_commit = "{}~1".format(starting_commit)

        iter_rev = "{0}...{1}".format(stopping_commit, starting_commit) if starting_commit else stopping_commit
        return iter_rev

    def _repository_is_empty(self):
        return not bool(self.repository.references)

    @staticmethod
    def _init_commit_tags_index(repo: Repo) -> Dict[Commit, List[TagReference]]:
        """ Create reverse index """
        reverse_tag_index = {}
        for tagref in repo.tags:
            commit = tagref.commit
            if commit not in reverse_tag_index:
                reverse_tag_index[commit] = []
            reverse_tag_index[commit].append(tagref)
        return reverse_tag_index

    @staticmethod
    def _extract_release_args(commit, tags) -> Tuple[str, Any, Any]:
        """ Extracts arguments for release """
        title = ", ".join(map(lambda tag: "{}".format(tag.name), tags))
        date_ = commit.authored_datetime.date()
        sha = commit.hexsha

        # TODO parse message, be carefull about commit message and tags message

        return title, date_, sha

    @staticmethod
    def _extract_note_args(commit) -> Tuple[str, str, str, str, str, str]:
        """ Extracts arguments for release Note from commit """
        sha = commit.hexsha
        message = commit.message
        type_, scope, description, body, footer, breaking_change = GitRepository._parse_conventional_commit(message)
        return sha, type_, description, scope, body, footer, breaking_change

    @staticmethod
    def _parse_conventional_commit(message: str) -> Tuple[str, str, str, str, str, str]:
        type_ = scope = breaking_flag = breaking_change = description = body = footer = ""

        msg_lines = message.splitlines(True)

        if len(msg_lines) > 0:
            # extract Headers
            # TODO this is less restrictive version of re. I have somewhere more restrictive one, maybe as option?
            type_, scope, breaking_flag, description = re.match(r"^(\w+)(\(\w+\))?(!)?: (.*)", msg_lines[0]).groups(
                default=""
            )

            # extract body and footers
            footer_found = False
            for line in msg_lines[1:]:
                if footer_found or GitRepository._is_footer_line(line):
                    footer_found = True
                    footer += line
                else:
                    body += line

        if scope:
            scope = scope[1:-1]
        if breaking_flag:
            breaking_change = description
        if body:
            body = body.strip()
        if footer:
            footer = footer.strip()
            match = re.match(r"BREAKING[ -]CHANGE: (.*)", footer)
            if match:
                breaking_change = match.groups(default="")[0]
                footer = ""

        return type_, scope, description, body, footer, breaking_change

    @staticmethod
    def _is_footer_line(line: str) -> bool:
        return re.match(r"\w+-?\w+?(: | #).*", line) or re.match(r"BREAKING[ -]CHANGE: .*", line)
