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
def open_changelog(test_repo):
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