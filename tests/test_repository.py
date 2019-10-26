import pytest
from unittest.mock import Mock
from unittest.mock import patch

from git import Repo, Commit

from auto_changelog.repository import GitRepository


@patch("auto_changelog.repository.Repo", autospec=True)
@patch.object(GitRepository, "_extract_release_args", return_value=("title", "date", "sha"))
@patch.object(GitRepository, "_extract_note_args", return_value=("sha", "change_type", "description"))
@patch.object(GitRepository, "_get_git_url", return_value="git@github.com:Michael-F-Bryan/auto-changelog.git")
def test_include_unreleased(mock_ggu, mock_ena, mock_era, mock_repo):
    mock_repo.return_value.iter_commits.return_value = [Mock(spec=Commit), Mock(spec=Commit)]

    repository = GitRepository(".", skip_unreleased=False)
    changelog = repository.generate_changelog()

    assert changelog.releases[0].title == "Unreleased"


@patch("auto_changelog.repository.Repo", autospec=True)
@patch.object(GitRepository, "_extract_release_args", return_value=("title", "date", "sha"))
@patch.object(GitRepository, "_extract_note_args", return_value=("sha", "change_type", "description"))
@patch.object(GitRepository, "_get_git_url", return_value="git@github.com:Michael-F-Bryan/auto-changelog.git")
def test_latest_version(mock_ggu, mock_ena, mock_era, mock_repo):
    mock_repo.return_value.iter_commits.return_value = [Mock(spec=Commit), Mock(spec=Commit)]

    repository = GitRepository(".", latest_version="v1.2.3")
    changelog = repository.generate_changelog()

    assert changelog.releases[0].title == "v1.2.3"


def test_index_init():
    commit1 = Mock()
    commit2 = Mock()
    tagref1 = Mock(commit=commit1)
    tagref2 = Mock(commit=commit2)
    tagref3 = Mock(commit=commit2)
    repo_mock = Mock(spec=Repo, tags=[tagref1, tagref2, tagref3])

    index = GitRepository._init_commit_tags_index(repo_mock)
    assert index == {commit1: [tagref1], commit2: [tagref2, tagref3]}


@pytest.mark.parametrize(
    "message, expected",
    [
        ("", ("", "", "", "", "")),
        ("feat: description", ("feat", "", "description", "", "")),
        ("feat(scope): description", ("feat", "scope", "description", "", "")),
        ("feat: description\n\nbody", ("feat", "", "description", "body", "")),
        ("feat: description\n\nbody\n\nfooter", ("feat", "", "description", "body", "footer")),
        ("feat(scope): description\n\nbody\n\nfooter", ("feat", "scope", "description", "body", "footer")),
    ],
)
def test_parse_conventional_commit_with_empty_message(message, expected):
    assert expected == GitRepository._parse_conventional_commit(message)


@patch("auto_changelog.repository.Repo", autospec=True)
@patch.object(GitRepository, "_get_git_url")
def test_get_remote_url(mock_ggu, mock_repo):
    mock_ggu.return_value = "git@github.com:Michael-F-Bryan/auto-changelog.git"
    remote_url = GitRepository(".")._remote_url(remote="origin")
    expected = "https://github.com/Michael-F-Bryan/auto-changelog"
    assert expected == remote_url
    mock_ggu.return_value = "https://github.com/Michael-F-Bryan/auto-changelog.git"
    remote_url = GitRepository(".")._remote_url(remote="origin")
    expected = "https://github.com/Michael-F-Bryan/auto-changelog"
    assert expected == remote_url


@patch("auto_changelog.repository.Repo", autospec=True)
@patch.object(GitRepository, "_remote_url", return_value='https://github.com/Michael-F-Bryan/auto-changelog')
def test_issue_from_git_remote_url(mock_ru, mock_repo):
    remote_url = GitRepository(".")._issue_from_git_remote_url(remote="origin")
    expected = "https://github.com/Michael-F-Bryan/auto-changelog/issues"
    assert expected == remote_url





