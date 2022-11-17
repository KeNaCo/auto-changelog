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
    global default_issue_pattern  # pylint: disable=global-statement
    global default_issue_url  # pylint: disable=global-statement
    global default_diff_url  # pylint: disable=global-statement
    global default_last_release  # pylint: disable=global-statement

    default_issue_pattern = gitlab_issue_pattern
    default_issue_url = gitlab_issue_url
    default_diff_url = gitlab_diff_url
    default_last_release = gitlab_last_release


def set_github():
    global default_issue_pattern  # pylint: disable=global-statement
    global default_issue_url  # pylint: disable=global-statement
    global default_diff_url  # pylint: disable=global-statement
    global default_last_release  # pylint: disable=global-statement

    default_issue_pattern = github_issue_pattern
    default_issue_url = github_issue_url
    default_diff_url = github_diff_url
    default_last_release = github_last_release
