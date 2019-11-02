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
        # shell argument fixes error for strings. Details in link below:
        # https://stackoverflow.com/questions/9935151/popen-error-errno-2-no-such-file-or-directory
        subprocess.run(command, shell=True)
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


@pytest.mark.parametrize(
    "commands",
    [
        [
            "git init -q",
            "touch file",
            "git add file",
            "git commit -m 'feat: Add file #1' -q",
            "git remote add upstream git@github.com:Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_remote(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--remote", "upstream", "--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "[#1](https://github.com/Michael-F-Bryan/auto-changelog/issues/1)" in changelog


@pytest.mark.parametrize(
    "commands", [["git init -q", "touch file", "git add file", "git commit -m 'feat: Add file #1' -q"]]
)
def test_option_latest_version(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--latest-version", "1.0.0"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "## 1.0.0" in changelog


@pytest.mark.parametrize(
    "commands", [["git init -q", "touch file", "git add file", "git commit -m 'feat: Add file #1' -q"]]
)
def test_option_unreleased(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "## Unreleased" in changelog


@pytest.mark.parametrize(
    "commands", [["git init -q", "touch file", "git add file", "git commit -m 'feat: Add file #1' -q"]]
)
def test_option_issue_url(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--issue-url", "issues.custom.com/{id}", "--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "[#1](issues.custom.com/1)" in changelog


@pytest.mark.parametrize(
    "commands", [["git init -q", "touch file", "git add file", "git commit -m 'feat: Add file PRO-1' -q"]]
)
def test_option_issue_pattern(test_repo, runner, open_changelog):
    result = runner.invoke(
        main, ["--issue-pattern", r" (\w\w\w-\d+)", "--issue-url", "issues.custom.com/{id}", "--unreleased"]
    )
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "[PRO-1](issues.custom.com/PRO-1)" in changelog


def test_option_stdout(test_repo, runner):
    result = runner.invoke(main, ["--stdout"])
    assert result.exit_code == 0, result.stderr
    assert "# Changelog" in result.output


@pytest.mark.parametrize(
    "commands",
    [
        [
            "git init -q",
            "touch file",
            "git add file",
            "git commit -m 'feat: Add file PRO-1' -q",
            "echo 'change' > file",
            "git add file",
            "git commit -m 'fix: Some file fix' -q",
            "git tag start",
        ]
    ],
)
def test_starting_commit(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--starting-commit", "start"])
    assert result.exit_code == 0, result.stderr
    changelog = open_changelog().read()
    assert "Add file PRO-1" not in changelog
    assert "Some file fix" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "git init -q",
            "touch file",
            "git add file",
            "git commit -m 'feat: Add file PRO-1' -q",
            "git tag stop",
            "echo 'change' > file",
            "git add file",
            "git commit -m 'fix: Some file fix' -q",
        ]
    ],
)
def test_stopping_commit(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--stopping-commit", "stop"])
    assert result.exit_code == 0, result.stderr
    changelog = open_changelog().read()
    assert "Add file PRO-1" in changelog
    assert "Some file fix" not in changelog
