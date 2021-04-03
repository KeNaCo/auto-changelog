import logging
import re
import auto_changelog
from datetime import date
from hashlib import sha256
from typing import Dict, List, Tuple, Any, Optional

from git import Repo, Commit, TagReference

from auto_changelog.domain_model import RepositoryInterface, Changelog, default_tag_pattern


class GitRepository(RepositoryInterface):
    def __init__(
        self,
        repository_path,
        latest_version: Optional[str] = None,
        skip_unreleased: bool = True,
        tag_prefix: str = "",
        tag_pattern: Optional[str] = None,
    ):
        self.repository = Repo(repository_path)
        self.tag_prefix = tag_prefix
        self.tag_pattern = tag_pattern
        self.commit_tags_index = self._init_commit_tags_index(self.repository, self.tag_prefix, self.tag_pattern)
        # in case of defined latest version, unreleased is used as latest release
        self._skip_unreleased = skip_unreleased and not bool(latest_version)
        self._latest_version = latest_version or None

    def generate_changelog(
        self,
        title: str = "Changelog",
        description: str = "",
        remote: str = "origin",
        issue_pattern: Optional[str] = None,
        issue_url: Optional[str] = None,
        diff_url: Optional[str] = None,
        starting_commit: str = "",
        stopping_commit: str = "HEAD",
    ) -> Changelog:
        locallogger = logging.getLogger("repository.generate_changelog")
        issue_url = issue_url or self._issue_from_git_remote_url(remote)
        diff_url = diff_url or self._diff_from_git_remote_url(remote)
        changelog = Changelog(title, description, issue_pattern, issue_url, self.tag_prefix, self.tag_pattern)
        if self._repository_is_empty():
            locallogger.info("Repository is empty.")
            return changelog
        iter_rev = self._get_iter_rev(starting_commit, stopping_commit)
        commits = self.repository.iter_commits(iter_rev)
        # Some thoughts here
        #  First we need to check if all commits are "released". If not, we have to create our special "Unreleased"
        #  release. Then we simply iter over all commits, assign them to current release or create new if we find it.
        first_commit = True
        skip = self._skip_unreleased
        locallogger.debug("Start iterating commits")
        for commit in commits:
            sha = commit.hexsha[0:7]
            locallogger.debug("Found commit {}".format(sha))

            if skip and commit not in self.commit_tags_index:
                locallogger.debug("Skipping unreleased commit " + sha)
                continue
            else:
                skip = False

            if first_commit and commit not in self.commit_tags_index:
                # if no last version specified by the user => consider HEAD
                if not self._latest_version:
                    locallogger.debug("Adding release 'unreleased'")
                    changelog.add_release("Unreleased", sha, date.today(), sha256())
                else:
                    locallogger.debug("Adding release '{}'".format(self._latest_version))
                    changelog.add_release(self._latest_version, self._latest_version, date.today(), sha256())
            first_commit = False

            if commit in self.commit_tags_index:
                attributes = self._extract_release_args(commit, self.commit_tags_index[commit])
                locallogger.debug("Adding release '{}' with attributes {}".format(attributes[0], attributes))
                changelog.add_release(*attributes)

            attributes = self._extract_note_args(commit)
            locallogger.debug("Adding commit {} with attributes {}".format(sha, attributes))
            changelog.add_note(*attributes)

        # create the compare url for each release
        releases = changelog.releases
        # we are using len(changelog.releases) - 1 because there is not compare url for the oldest version
        if diff_url is not None:  # if links are off
            for release_index in reversed(range(len(changelog.releases) - 1)):
                releases[release_index].set_compare_url(diff_url, releases[release_index + 1].title)

        # Close the link to the repository
        # If we are not closing it, some references are not cleaned on windows
        self.repository.close()

        return changelog

    def _issue_from_git_remote_url(self, remote: str) -> Optional[str]:
        """ Creates issue url with {id} format key """
        try:
            url = self._remote_url(remote)
            return auto_changelog.default_issue_url.format(base_url=url)
        except ValueError as e:
            logging.error("%s. Turning off issue links.", e)
            return None

    def _diff_from_git_remote_url(self, remote: str):
        try:
            url = self._remote_url(remote)
            return auto_changelog.default_diff_url.format(base_url=url)
        except ValueError as e:
            logging.error("%s. Turning off compare url links.", e)
            return None

    def _remote_url(self, remote: str) -> str:
        """ Extract remote url from remote url """
        url = self._get_git_url(remote=remote)
        url = GitRepository._sanitize_remote_url(url)
        return url

    @staticmethod
    def _sanitize_remote_url(remote: str) -> str:
        # 'git@github.com:Michael-F-Bryan/auto-changelog.git' -> 'https://github.com/Michael-F-Bryan/auto-changelog'
        # 'https://github.com/Michael-F-Bryan/auto-changelog.git' -> 'https://github.com/Michael-F-Bryan/auto-changelog'
        return re.sub(r"^(https|git|ssh)(:\/\/|@)(.*@)?([^\/:]+)[\/:]([^\/:]+)\/(.+).git$", r"https://\4/\5/\6", remote)

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
    def _init_commit_tags_index(
        repo: Repo, tag_prefix: str, tag_pattern: Optional[str] = None
    ) -> Dict[Commit, List[TagReference]]:
        """ Create reverse index """
        reverse_tag_index = {}
        semver_regex = default_tag_pattern
        for tagref in repo.tags:
            tag_name = tagref.name
            commit = tagref.commit

            consider_tag = False

            # consider & remove the prefix if we found one
            if tag_name.startswith(tag_prefix):
                tag_name = tag_name.replace(tag_prefix, "")

                # if user specified a tag pattern => consider it
                if tag_pattern is not None:
                    if re.fullmatch(tag_pattern, tag_name):
                        consider_tag = True
                # no tag pattern specified by user => check semver semantic
                elif re.fullmatch(semver_regex, tag_name):
                    consider_tag = True

            # good format of the tag => consider it
            if consider_tag:
                if commit not in reverse_tag_index:
                    reverse_tag_index[commit] = []
                reverse_tag_index[commit].append(tagref)
        return reverse_tag_index

    @staticmethod
    def _extract_release_args(commit, tags) -> Tuple[str, str, Any, Any]:
        """ Extracts arguments for release """
        title = ", ".join(map(lambda tag: "{}".format(tag.name), tags))
        date_ = commit.authored_datetime.date()
        sha = commit.hexsha

        # TODO parse message, be carefull about commit message and tags message

        return title, title, date_, sha

    @staticmethod
    def _extract_note_args(commit) -> Tuple[str, str, str, str, str, str]:
        """ Extracts arguments for release Note from commit """
        sha = commit.hexsha
        message = commit.message
        type_, scope, description, body, footer = GitRepository._parse_conventional_commit(message)
        return sha, type_, description, scope, body, footer

    @staticmethod
    def _parse_conventional_commit(message: str) -> Tuple[str, str, str, str, str]:
        type_ = scope = description = body_footer = body = footer = ""
        # TODO this is less restrictive version of re. I have somewhere more restrictive one, maybe as option?
        match = re.match(r"^(\w+)(\(\w+\))?!?: (.*)(\n\n[\w\W]*)?$", message.strip())
        if match:
            type_, scope, description, body_footer = match.groups(default="")
        else:
            locallogger = logging.getLogger("repository._parse_conventional_commit")
            locallogger.debug("Commit message did not match expected pattern: {}".format(message))
        if scope:
            scope = scope[1:-1]
        if body_footer:
            bf_match = re.match(r"^(\n\n[\w\W]+?)?(\n\n([a-zA-Z-]+|BREAKING[- ]CHANGE)(: | #)[\w\W]+)$", body_footer)
            if bf_match:
                result = bf_match.groups(default="")
                body = result[0][2:]
                footer = result[1][2:]
            else:
                body = body_footer[2:]
        return type_, scope, description, body, footer
