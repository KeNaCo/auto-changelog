import pytest
from textwrap import dedent

from auto_changelog.domain_model import Changelog
from auto_changelog.presenter import MarkdownPresenter


@pytest.fixture(params=['', 'Title'])
def title(request):
    return request.param


@pytest.fixture(params=['', 'Description'])
def description(request):
    return request.param


@pytest.fixture
def empty_changelog(title, description):
    return Changelog(title, description)


@pytest.fixture
def changelog(title, description):
    return Changelog(title, description)


@pytest.fixture
def markdown_presenter():
    return MarkdownPresenter()


def test_markdown_presenter_empty_changelog(empty_changelog, markdown_presenter):
    markdown = markdown_presenter.present(empty_changelog)
    assert '# {}\n\n{}'.format(empty_changelog.title, empty_changelog.description) in markdown


def test_markdown_presenter_changelog_with_features(changelog, markdown_presenter):
    changelog.add_release('Unreleased', None, None)
    changelog.add_note('', 'feat', 'description')
    changelog.add_note('', 'feat', 'description', scope='scope')
    description = '{}\n'.format(changelog.description) if changelog.description else ''
    assert_markdown = dedent('''\
    # {}
    
    {}
    ## Unreleased
    
    #### Features
    
    * description
    * (scope): description
    '''.format(changelog.title, description))
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown in markdown


def test_markdown_presenter_changelog_with_features(changelog, markdown_presenter):
    changelog.add_release('Unreleased', None, None)
    changelog.add_note('', 'fix', 'description')
    changelog.add_note('', 'fix', 'description', scope='scope')
    description = '{}\n'.format(changelog.description) if changelog.description else ''
    assert_markdown = dedent('''\
    # {}

    {}
    ## Unreleased

    #### Fixes

    * description
    * (scope): description
    '''.format(changelog.title, description))
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown in markdown