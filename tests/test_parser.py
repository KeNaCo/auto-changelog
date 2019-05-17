import os
import pytest

from git import Repo

from auto_changelog.parser import create_reverse_tag_index

TEST_DIR_PATH = os.path.dirname(__file__)


# FIXME I need to find some easy way to create repos for testing in python.
#  I am not willing to do this right now, so just to keep some note.

# @pytest.fixture
# def empty_repo(request):
#     return Repo(path=os.path.join(TEST_DIR_PATH, 'test-git-repo-empty'))
#
#
# @pytest.fixture
# def one_tag_repo(request):
#     return Repo(path=os.path.join(TEST_DIR_PATH, 'test-git-repo-one-tag'))
#
#
# def test_create_tag_index_from_empty_repo(empty_repo):
#     assert create_reverse_tag_index(empty_repo) == {}
#
#
# def test_create_tag_index_from_one_tag_repo(one_tag_repo):
#     reversed_index = create_reverse_tag_index(one_tag_repo)
#     assert len(reversed_index) == 1
