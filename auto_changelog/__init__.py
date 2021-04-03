from typing import Any

from auto_changelog.domain_model import RepositoryInterface, PresenterInterface

__version__ = "1.0.0dev1"

github_issue_pattern = r"(#([\w-]+))"
github_issue_url = "{base_url}/issues/{{id}}"
github_diff_url = "{base_url}/compare/{{previous}}...{{current}}"
github_last_release = "HEAD"

gitlab_issue_pattern = r"(\!([\w-]+))"
gitlab_issue_url = "{base_url}/-/merge_requests/{{id}}"
gitlab_diff_url = "{base_url}/-/compare/{{previous}}...{{current}}"
gitlab_last_release = "master"

default_issue_pattern = github_issue_pattern
default_issue_url = github_issue_url
default_diff_url = github_diff_url
default_last_release = github_last_release


def set_gitlab():
    global default_issue_pattern
    global default_issue_url
    global default_diff_url
    global default_last_release

    default_issue_pattern = gitlab_issue_pattern
    default_issue_url = gitlab_issue_url
    default_diff_url = gitlab_diff_url
    default_last_release = gitlab_last_release


def set_github():
    global default_issue_pattern
    global default_issue_url
    global default_diff_url
    global default_last_release

    default_issue_pattern = github_issue_pattern
    default_issue_url = github_issue_url
    default_diff_url = github_diff_url
    default_last_release = github_last_release


def generate_changelog(repository: RepositoryInterface, presenter: PresenterInterface, *args, **kwargs) -> Any:
    """ Use-case function coordinates repository and interface """
    changelog = repository.generate_changelog(*args, **kwargs)
    return presenter.present(changelog)
