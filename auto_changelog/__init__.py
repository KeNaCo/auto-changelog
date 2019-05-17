from typing import Any

from auto_changelog.domain_model import RepositoryInterface, PresenterInterface

__version__ = '0.2.0'


def generate_changelog(
        repository: RepositoryInterface,
        presenter: PresenterInterface,
        title: str = 'Changelog',
        description: str = ''
) -> Any:
    """ Use-case function coordinates repository and interface """
    changelog = repository.generate_changelog(title, description)
    return presenter.present(changelog)
