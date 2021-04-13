import logging
import auto_changelog
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Union, List, Optional, Tuple, Any

# Default aim for Semver tags.
# Original Semver source: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
default_tag_pattern = r"(?P<version>((?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*))(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)"  # noqa: E501


class ChangeType(Enum):
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    DOCS = "docs"
    FEAT = "feat"
    FIX = "fix"
    PERF = "perf"
    REFACTOR = "refactor"
    REVERT = "revert"
    STYLE = "style"
    TEST = "test"


class Note:
    def __init__(
        self,
        sha: str,
        change_type: Union[ChangeType, str],
        description: str,
        scope: str = "",
        body: str = "",
        footer: str = "",
    ):
        self.sha = sha
        self.change_type = ChangeType(change_type) if change_type else change_type  # TODO Hmm..
        self.scope = scope
        self.description = description
        self.body = body
        self.footer = footer

    def __eq__(self, other):
        return (
            self.sha == other.sha
            and self.change_type == other.change_type
            and self.description == other.description
            and self.body == other.body
            and self.footer == other.footer
        )


class Release(Note):
    def __init__(self, title, tag, date, sha, change_type="chore", description="", *args, **kwargs):
        super(Release, self).__init__(sha, change_type, description, *args, **kwargs)
        self.title = title
        self.tag = tag
        self.date = date
        self._notes = []  # type: List[Note]
        self._changes_indicators = {type_: False for type_ in ChangeType}
        self.diff_url = None
        self.previous_tag = None

    @property
    def builds(self):
        return self._notes_with_type(ChangeType.BUILD)

    @property
    def ci(self):
        return self._notes_with_type(ChangeType.CI)

    @property
    def chore(self):
        return self._notes_with_type(ChangeType.CHORE)

    @property
    def docs(self):
        return self._notes_with_type(ChangeType.DOCS)

    @property
    def features(self):
        return self._notes_with_type(ChangeType.FEAT)

    @property
    def fixes(self):
        return self._notes_with_type(ChangeType.FIX)

    @property
    def performance_improvements(self):
        return self._notes_with_type(ChangeType.PERF)

    @property
    def refactorings(self):
        return self._notes_with_type(ChangeType.REFACTOR)

    @property
    def reverts(self):
        return self._notes_with_type(ChangeType.REVERT)

    @property
    def style_changes(self):
        return self._notes_with_type(ChangeType.STYLE)

    @property
    def tests(self):
        return self._notes_with_type(ChangeType.TEST)

    @property
    def has_builds(self):
        return self._has(ChangeType.BUILD)

    @property
    def has_ci(self):
        return self._has(ChangeType.CI)

    @property
    def has_chore(self):
        return self._has(ChangeType.CHORE)

    @property
    def has_docs(self):
        return self._has(ChangeType.DOCS)

    @property
    def has_features(self):
        return self._has(ChangeType.FEAT)

    @property
    def has_fixes(self):
        return self._has(ChangeType.FIX)

    @property
    def has_performance_improvements(self):
        return self._has(ChangeType.PERF)

    @property
    def has_refactorings(self):
        return self._has(ChangeType.REFACTOR)

    @property
    def has_reverts(self):
        return self._has(ChangeType.REVERT)

    @property
    def has_style_changes(self):
        return self._has(ChangeType.STYLE)

    @property
    def has_tests(self):
        return self._has(ChangeType.TEST)

    def add_note(self, note: Note):
        self._notes.append(note)
        self._changes_indicators[note.change_type] = True

    def set_compare_url(self, diff_url: str, previous_tag: str):
        self.previous_tag = previous_tag
        self.diff_url = diff_url.format(previous=previous_tag, current=self.tag)

    def _notes_with(self, predicate: Callable) -> Tuple[Note]:
        return tuple(filter(predicate, self._notes))

    def _notes_with_type(self, type_: ChangeType) -> Tuple[Note]:
        return self._notes_with(lambda x: x.change_type == type_)

    def _has(self, type_: ChangeType) -> bool:
        return type_ in self._changes_indicators


class Changelog:
    def __init__(
        self,
        title: str = "Changelog",
        description: str = "",
        issue_pattern: Optional[str] = None,
        issue_url: Optional[str] = None,
        tag_prefix: str = "",
        tag_pattern: Optional[str] = None,
    ):
        self.title = title
        self.description = description
        logging.debug(auto_changelog.default_issue_pattern)
        self.issue_pattern = issue_pattern or auto_changelog.default_issue_pattern
        logging.debug(self.issue_pattern)
        self.issue_url = issue_url or ""
        logging.debug(issue_url)
        logging.debug(self.issue_url)
        self.tag_prefix = tag_prefix
        self.tag_pattern = tag_pattern or default_tag_pattern
        self._releases = []  # type: List[Release]
        self._current_release = None  # type: Optional[Release]

    def add_release(self, *args, **kwargs):
        """ Add new Release. Require same arguments as :class:`Release` """
        release = Release(*args, **kwargs)
        self._releases.append(release)
        self._current_release = release

    def add_note(self, *args, **kwargs):
        """ Add new Note to current release. Require same arguments as :class:`Note` """
        try:
            note = Note(*args, **kwargs)
        except ValueError as err:
            # Ignore exceptions raised by unsupported commit type.
            locallogger = logging.getLogger("Changelog.add_note")
            locallogger.debug("Ignore exception raised by unsupported commit: {}".format(err))
            return

        if not self._current_release:
            raise ValueError("There is no release, note can be added to")
        self._current_release.add_note(note)

    @property
    def releases(self) -> Tuple[Release]:
        """ Returns iterable of releases sorted by date (newer first)"""
        return tuple(sorted(self._releases, key=lambda r: r.date, reverse=True))


class RepositoryInterface(ABC):
    @abstractmethod
    def generate_changelog(
        self,
        title: str,
        description: str,
        remote: str,
        issue_pattern: Optional[str],
        issue_url: Optional[str],
        diff_url: Optional[str],
        starting_commit: str,
        stopping_commit: str,
    ) -> Changelog:
        raise NotImplementedError


class PresenterInterface(ABC):
    @abstractmethod
    def present(self, changelog: Changelog) -> Any:
        raise NotImplementedError
