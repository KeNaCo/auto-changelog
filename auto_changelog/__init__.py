from typing import Any

from auto_changelog.domain_model import RepositoryInterface, PresenterInterface

__version__ = "1.0.0dev1"


def generate_changelog(repository: RepositoryInterface, presenter: PresenterInterface, *args, **kwargs) -> Any:
    """ Use-case function coordinates repository and interface """
    changelog = repository.generate_changelog(*args, **kwargs)
    return presenter.present(changelog)
