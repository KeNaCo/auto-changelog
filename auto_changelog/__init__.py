from typing import Any

from auto_changelog.domain_model import RepositoryInterface, PresenterInterface


def generate_changelog(repository: RepositoryInterface, presenter: PresenterInterface) -> Any:
    """ Use-case function coordinates repository and interface """
    changelog = repository.generate_changelog()
    return presenter.present(changelog)
