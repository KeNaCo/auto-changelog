import re
from datetime import date
from hashlib import sha256
from typing import Dict, List, Tuple, Any

from git import Repo, Commit, TagReference

from auto_changelog.domain_model import RepositoryInterface, Changelog


class GitRepository(RepositoryInterface):
    def __init__(self, repository_path, *, skip_unreleased: bool = True):
        self.repository = Repo(repository_path)
        self.commit_tags_index = self._init_commit_tags_index(self.repository)
        self._skip_unreleased = skip_unreleased

    def generate_changelog(self, title: str = 'Changelog', description: str = '', starting_commit: str = '', stopping_commit: str = 'HEAD') -> Changelog:
        changelog = Changelog(title, description)
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
                changelog.add_release('Unreleased', date.today(), sha256())
            first_commit = False

            if commit in self.commit_tags_index:
                attributes = self._extract_release_args(commit, self.commit_tags_index[commit])
                changelog.add_release(*attributes)

            attributes = self._extract_note_args(commit)
            changelog.add_note(*attributes)
        return changelog

    def _get_iter_rev(self, starting_commit: str, stopping_commit: str):
        if starting_commit:
            c = self.repository.commit(starting_commit)
            if not c.parents:
                # starting_commit is initial commit,
                # treat as default
                starting_commit = ''
            else:
                # iter_commits iters from the first rev to the second rev,
                # but not contains the second rev.
                # Here we set the second rev to its previous one then the
                # second rev would be included.
                starting_commit = '{}~1'.format(starting_commit)

        iter_rev = '{0}...{1}'.format(stopping_commit, starting_commit) if starting_commit else stopping_commit
        return iter_rev

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
        title = ', '.join(map(lambda tag: '{}'.format(tag.name), tags))
        date_ = date.today()
        sha = commit.hexsha

        # TODO parse message, be carefull about commit message and tags message

        return title, date_, sha

    @staticmethod
    def _extract_note_args(commit) -> Tuple[str, str, str, str, str, str]:
        """ Extracts arguments for release Note from commit """
        sha = commit.hexsha
        message = commit.message
        type_, scope, description, body, footer = GitRepository._parse_conventional_commit(message)
        return sha, type_, description, scope, body, footer

    @staticmethod
    def _parse_conventional_commit(message: str) -> Tuple[str, str, str, str, str]:
        type_ = scope = description = body = footer = ''
        # TODO this is less restrictive version of re. I have somewhere more restrictive one, maybe as option?
        match = re.match(r'^(\w+)(\(\w+\))?: (.*)(\n\n.+)?(\n\n.+)?$', message)
        if match:
            type_, scope, description, body, footer = match.groups(default='')
        if scope:
            scope = scope[1:-1]
        if body:
            body = body[2:]
        if footer:
            footer = footer[2:]
        return type_, scope, description, body, footer
