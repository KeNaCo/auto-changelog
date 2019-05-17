import pytest
from unittest.mock import Mock
from textwrap import dedent

from git import Repo

from auto_changelog.repository import GitRepository


def test_index_init():
    commit1 = Mock()
    commit2 = Mock()
    tagref1 = Mock(commit=commit1)
    tagref2 = Mock(commit=commit2)
    tagref3 = Mock(commit=commit2)
    repo_mock = Mock(spec=Repo, tags=[tagref1, tagref2, tagref3])

    index = GitRepository._init_commit_tags_index(repo_mock)
    assert index == {commit1: [tagref1], commit2: [tagref2, tagref3]}


@pytest.mark.parametrize('message, expected', [
    ("", ("", "", "", "", "")),
    ("feat: description", ("feat", "", "description", "", "")),
    ("feat(scope): description", ("feat", "scope", "description", "", "")),
    ("feat: description\n\nbody", ("feat", "", "description", "body", "")),
    ("feat: description\n\nbody\n\nfooter", ("feat", "", "description", "body", "footer")),
    ("feat(scope): description\n\nbody\n\nfooter", ("feat", "scope", "description", "body", "footer")),
])
def test_parse_conventional_commit_with_empty_message(message, expected):
    assert expected == GitRepository._parse_conventional_commit(message)
