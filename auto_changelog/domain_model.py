from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Union

default_issue_pattern = r"(#([\w-]+))"


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
        breaking_change: str = "",
    ):
        self.sha = sha
        self.change_type = ChangeType(change_type) if change_type else change_type  # TODO Hmm..
        self.scope = scope
        self.description = description
        self.body = body
        self.footer = footer
        self.breaking_change = breaking_change

    def __eq__(self, other):
        return (
            self.sha == other.sha
            and self.change_type == other.change_type
            and self.description == other.description
            and self.body == other.body
            and self.footer == other.footer
            and self.breaking_change == other.breaking_change
        )


class Release(Note):
    def __init__(self, title, date, sha, change_type="chore", description="", *args, **kwargs):
        super(Release, self).__init__(sha, change_type, description, *args, **kwargs)
        self.title = title
        self.date = date
        self._notes = []  # type: List[Note]
        self._changes_indicators = {type_: False for type_ in ChangeType}

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
    def breaking_changes(self):
        return self._notes_with(lambda x: x.breaking_change)

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
    ):
        self.title = title
        self.description = description
        self.issue_pattern = issue_pattern or default_issue_pattern
        self.issue_url = issue_url or ""
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
        except ValueError:
            # Ignore exceptions raised by unsupported commit type.
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
        starting_commit: str,
        stopping_commit: str,
    ) -> Changelog:
        raise NotImplementedError


class PresenterInterface(ABC):
    @abstractmethod
    def present(self, changelog: Changelog) -> Any:
        raise NotImplementedError
