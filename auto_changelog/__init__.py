from typing import Any

from auto_changelog.domain_model import RepositoryInterface, PresenterInterface

__version__ = '1.0.0dev1'


def generate_changelog(
        repository: RepositoryInterface,
        presenter: PresenterInterface,
        title: str = 'Changelog',
        description: str = '',
        starting_commit: str = '',
        stopping_commit: str = 'HEAD',
) -> Any:
    """ Use-case function coordinates repository and interface """
    changelog = repository.generate_changelog(title, description, starting_commit=starting_commit, stopping_commit=stopping_commit)
    return presenter.present(changelog)
