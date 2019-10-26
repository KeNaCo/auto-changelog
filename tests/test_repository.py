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
    tagref1.name = "1.0.0"
    tagref2 = Mock(commit=commit2)
    tagref2.name = "2.0.0"
    tagref3 = Mock(commit=commit2)
    tagref3.name = "2.0.0"

    repo_mock = Mock(spec=Repo, tags=[tagref1, tagref2, tagref3])

    # no prefix
    tag_prefix = ""
    # we are using default tag pattern => semantic versioning
    tag_pattern = None

    index = GitRepository._init_commit_tags_index(repo_mock, tag_prefix, tag_pattern)
    assert index == {commit1: [tagref1], commit2: [tagref2, tagref3]}


@pytest.mark.parametrize("tags", [["1.0.0", "1.0.0-beta", "v2.0.0", "v3.0.0", "4.0", "5", "v6"]])
@pytest.mark.parametrize(
    "tag_prefix, tag_pattern, expected_tags",
    [
        ("", None, ["1.0.0", "1.0.0-beta"]),
        ("v", None, ["v2.0.0", "v3.0.0"]),
        ("x", None, []),
        ("", "([1-9])", ["5"]),
        ("v", "([1-9])", ["v6"]),
        ("x", "([1-9])", []),
    ],
)
def test_tag_pattern(tags, tag_prefix, tag_pattern, expected_tags):
    tag_refs = []
    for tag in tags:
        tag_ref = Mock(commit=Mock())
        tag_ref.name = tag
        tag_refs.append(tag_ref)

    repo_mock = Mock(spec=Repo, tags=tag_refs)

    selected_tag_refs = GitRepository._init_commit_tags_index(repo_mock, tag_prefix, tag_pattern)

    selected_tags = []
    for selected_tag_ref_list in selected_tag_refs.values():
        for selected_tag_ref in selected_tag_ref_list:
            selected_tags.append(selected_tag_ref.name)

    assert selected_tags == expected_tags


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
@patch.object(GitRepository, "_remote_url", return_value="https://github.com/Michael-F-Bryan/auto-changelog")
def test_issue_from_git_remote_url(mock_ru, mock_repo):
    remote_url = GitRepository(".")._issue_from_git_remote_url(remote="origin")
    expected = "https://github.com/Michael-F-Bryan/auto-changelog/issues/{id}"
    assert expected == remote_url
