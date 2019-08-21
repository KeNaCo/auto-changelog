from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Union, List, Optional, Tuple, Any


class ChangeType(Enum):
    BUILD = 'build'
    CI = 'ci'
    CHORE = 'chore'
    DOCS = 'docs'
    FEAT = 'feat'
    FIX = 'fix'
    PERF = 'perf'
    REFACTOR = 'refactor'
    REVERT = 'revert'
    STYLE = 'style'
    TEST = 'test'


class Note:
    def __init__(self, sha: str, change_type: Union[ChangeType, str], description: str,
                 scope: str = '', body: str = '', footer: str = ''):
        self.sha = sha
        self.change_type = ChangeType(change_type) if change_type else change_type  # TODO Hmm..
        self.scope = scope
        self.description = description
        self.body = body
        self.footer = footer

    def __eq__(self, other):
        return self.sha == other.sha \
               and self.change_type == other.change_type \
               and self.description == other.description \
               and self.body == other.body \
               and self.footer == other.footer


class Release(Note):
    def __init__(self, title, date, sha, change_type='chore', description='', *args, **kwargs):
        super(Release, self).__init__(sha, change_type, description, *args, **kwargs)
        self.title = title
        self.date = date
        self._notes = []  # type: List[Note]
        self._changes_indicators = {type_: False for type_ in ChangeType}

    @property
    def features(self):
        return self._notes_with_type(ChangeType.FEAT)

    @property
    def fixes(self):
        return self._notes_with_type(ChangeType.FIX)

    @property
    def has_features(self):
        return self._has(ChangeType.FEAT)

    @property
    def has_fixes(self):
        return self._has(ChangeType.FIX)

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
    def __init__(self, title: str = 'Changelog', description: str = ''):
        self.title = title
        self.description = description
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
            raise ValueError('There is no release, note can be added to')
        self._current_release.add_note(note)

    @property
    def releases(self) -> Tuple[Release]:
        """ Returns iterable of releases sorted by date (newer first)"""
        return tuple(sorted(self._releases, key=lambda r: r.date, reverse=True))


class RepositoryInterface(ABC):
    @abstractmethod
    def generate_changelog(self, title: str, description: str, starting_commit: str, stopping_commit: str) -> Changelog:
        raise NotImplementedError


class PresenterInterface(ABC):
    @abstractmethod
    def present(self, changelog: Changelog) -> Any:
        raise NotImplementedError
