import os
import pytest
import subprocess

from click.testing import CliRunner

from auto_changelog.__main__ import main


@pytest.fixture
def commands():
    return ["git init -q"]


@pytest.fixture
def test_repo(tmp_path, commands):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    for command in commands:
        subprocess.run(command.split())
    yield tmp_path
    os.chdir(cwd)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def changelog_name():
    return "CHANGELOG.md"


@pytest.fixture
def open_changelog(test_repo, changelog_name):
    file = None

    def _open_changelog():
        nonlocal file
        file = open(changelog_name, "r")
        return file

    yield _open_changelog

    if file:
        file.close()


def test_empty_repo(test_repo, runner, open_changelog):
    result = runner.invoke(main)
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert changelog == "# Changelog\n"


def test_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.stderr
    assert result.output


def test_option_repo(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--repo", test_repo])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert changelog


def test_option_title(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--title", "Title"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "# Title\n" == changelog


def test_option_description(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--description", "My description"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "My description\n" in changelog


@pytest.mark.parametrize("changelog_name", ["a.out"])
def test_option_output(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--output", "a.out"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert changelog
