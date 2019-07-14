import pytest
from datetime import date, timedelta

from auto_changelog.domain_model import Changelog


def test_empty_changelog():
    changelog = Changelog()
    assert changelog.title == 'Changelog'
    assert changelog.description == ''
    assert changelog.releases == tuple()


def test_changelog_add_note_without_release():
    changelog = Changelog()
    with pytest.raises(ValueError):
        changelog.add_note(sha='', change_type='feat', description='')


def test_changelog_add_note():
    changelog = Changelog()
    changelog.add_release(title='Unreleased', date=date.today(), sha='')
    changelog.add_note(sha='123', change_type='fix', description='')
    changelog.add_note(sha='345', change_type='feat', description='')
    # unsupported_type should be ignored
    changelog.add_note(sha='567', change_type='unsupported_type', description='')

    releases = changelog.releases
    assert len(releases) == 1
    assert releases[0].title == 'Unreleased'
    assert len(releases[0].fixes) == 1
    assert releases[0].fixes[0].sha == '123'
    assert len(releases[0].features) == 1
    assert releases[0].features[0].sha == '345'
    assert len(releases[0]._notes) == 2


def test_changelog_sorted_releases():
    changelog = Changelog()
    changelog.add_release(title='1.2.3', date=date.today(), sha='123')
    changelog.add_release(title='1.1.1', date=date.today()-timedelta(days=1), sha='456')
    releases = changelog.releases

    assert len(releases) == 2
    assert releases[0].title == '1.2.3'
    assert releases[1].title == '1.1.1'
