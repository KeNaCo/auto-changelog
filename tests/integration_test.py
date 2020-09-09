import logging
import os
import pytest
import subprocess

from click.testing import CliRunner

from auto_changelog.__main__ import main


@pytest.fixture
def commands():
    return []


@pytest.fixture
def test_repo(tmp_path, commands):
    cwd = os.getcwd()
    os.chdir(str(tmp_path))
    init_commands = ["git init -q", "git config user.name 'John Doe'", "git config user.email john.doe@email"]
    for command in init_commands + commands:
        # shell argument fixes error for strings. Details in link below:
        # https://stackoverflow.com/questions/9935151/popen-error-errno-2-no-such-file-or-directory
        subprocess.run(command, shell=True)
    yield str(tmp_path)
    os.chdir(cwd)


@pytest.fixture
def runner():
    return CliRunner(mix_stderr=False)


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


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_empty_repo(runner, open_changelog):
    result = runner.invoke(main)
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert changelog == "# Changelog\n"


def test_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.stderr
    assert result.output


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_option_repo(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--repo", test_repo])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert changelog


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_option_title(runner, open_changelog):
    result = runner.invoke(main, ["--title", "Title"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "# Title\n" == changelog


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_option_description(runner, open_changelog):
    result = runner.invoke(main, ["--description", "My description"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "My description\n" in changelog


@pytest.mark.parametrize("changelog_name", ["a.out"])
@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_option_output(runner, open_changelog):
    result = runner.invoke(main, ["--output", "a.out"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1" -q',
            "git remote add upstream git@github.com:Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_remote(runner, open_changelog):
    result = runner.invoke(main, ["--remote", "upstream", "--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "[#1](https://github.com/Michael-F-Bryan/auto-changelog/issues/1)" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_latest_version(runner, open_changelog):
    result = runner.invoke(main, ["--latest-version", "1.0.0"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "## 1.0.0" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_unreleased(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "## Unreleased" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_skipping_unreleased(runner, open_changelog):
    result = runner.invoke(main)
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "## Unreleased" not in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_issue_url(runner, open_changelog):
    result = runner.invoke(main, ["--issue-url", "issues.custom.com/{id}", "--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "[#1](issues.custom.com/1)" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file PRO-1" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_issue_pattern(runner, open_changelog):
    result = runner.invoke(
        main, ["--issue-pattern", r" (\w\w\w-\d+)", "--issue-url", "issues.custom.com/{id}", "--unreleased"]
    )
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    assert "[PRO-1](issues.custom.com/PRO-1)" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file PRO-1" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_invalid_issue_pattern(runner, open_changelog):
    result = runner.invoke(
        main, ["--issue-pattern", r" \w\w\w-\d+", "--issue-url", "issues.custom.com/{id}", "--unreleased"]
    )
    assert result.exit_code != 0, result.stderr


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_option_stdout(runner, open_changelog):
    result = runner.invoke(main, ["--stdout"])
    assert result.exit_code == 0, result.stderr
    assert "# Changelog" in result.output


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file" -q',
            "git tag custom-tag",
            'echo "change" > file',
            "git add file",
            'git commit -m "chore: Change" -q',
            "git tag 1.0.0",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_tag_pattern(runner, open_changelog):
    result = runner.invoke(main, ["--tag-pattern", r"\d+.\d+.\d+"])
    assert result.exit_code == 0, result.stderr
    changelog = open_changelog().read()
    assert "1.0.0" in changelog
    assert "custom-tag" not in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file" -q',
            "git tag v-something",
            'echo "change" > file',
            "git add file",
            'git commit -m "chore: Change" -q',
            "git tag 1.0.0",
            "git tag v2.0.0",
            'echo "change2" > file',
            "git add file",
            'git commit -m "chore: Change2" -q',
            "git tag v3.0.0",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_option_tag_prefix(runner, open_changelog):
    result = runner.invoke(main, ["--tag-prefix", "v"])
    assert result.exit_code == 0, result.exc_info
    changelog = open_changelog().read()
    assert "1.0.0" not in changelog
    assert "v-something" not in changelog
    assert "v2.0.0" in changelog
    assert "v3.0.0" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file" -q',
            "git tag release-1",
            'echo "change" > file',
            "git add file",
            'git commit -m "chore: Change" -q',
            "git tag 1",
            "git tag release-1.2.3",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_tag_prefix_and_pattern_combination(runner, open_changelog):
    result = runner.invoke(main, ["--tag-prefix", "release-", "--tag-pattern", r"\d"])
    assert result.exit_code == 0, result.stderr
    changelog = open_changelog().read()
    assert "release-1" in changelog
    assert "## 1 " not in changelog
    assert "release-1.2.3" not in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file PRO-1" -q',
            "echo 'change' > file",
            "git add file",
            'git commit -m "fix: Some file fix" -q',
            "git tag start",
            "git tag 1.0.0",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
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
            "echo test > file",
            "git add file",
            'git commit -m "fix: Some file fix" -q',
            "git tag 1.0.0",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_starting_commit_is_only_commit(runner, open_changelog):
    result = runner.invoke(main, ["--starting-commit", "1.0.0"])
    assert result.exit_code == 0, result.stderr
    changelog = open_changelog().read()
    assert "Some file fix" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "fix: Some file fix" -q',
            "git tag 1.0.0",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_starting_commit_not_exist(test_repo, runner, open_changelog):
    result = runner.invoke(main, ["--starting-commit", "nonexist"])
    assert result.exit_code != 0, result.stderr


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file PRO-1" -q',
            "git tag stop",
            'echo "change" > file',
            "git add file",
            'git commit -m "fix: Some file fix" -q',
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_stopping_commit(runner, open_changelog):
    result = runner.invoke(main, ["--stopping-commit", "stop", "--unreleased"])
    assert result.exit_code == 0, result.stderr
    changelog = open_changelog().read()
    assert "Add file PRO-1" in changelog
    assert "Some file fix" not in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1\n\nBody line" -q',
            "git log",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_single_line_body(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    print(changelog)
    assert "Add file [#1]" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1\n\nBody line 1\nBody line 2" -q',
            "git log",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_double_line_body(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    print(changelog)
    assert "Add file [#1]" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1\n\nBody line 1\nBody line 2\nBody line 3" -q',
            "git log",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_triple_line_body(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    print(changelog)
    assert "Add file [#1]" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1\n\nBody paragraph 1\n\nBody paragraph 2" -q',
            "git log",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_multi_paragraph_body(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    print(changelog)
    assert "Add file [#1]" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1\n\nBody line\n\nFooter: first footer" -q',
            "git log",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_single_line_body_single_footer(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    print(changelog)
    assert "Add file [#1]" in changelog


@pytest.mark.parametrize(
    "commands",
    [
        [
            "echo test > file",
            "git add file",
            'git commit -m "feat: Add file #1\n\nBody line\n\nFooter: first footer\nFooter: second footer" -q',
            "git log",
            "git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git",
        ]
    ],
)
def test_single_line_body_double_footer(runner, open_changelog):
    result = runner.invoke(main, ["--unreleased"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    changelog = open_changelog().read()
    print(changelog)
    assert "Add file [#1]" in changelog


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_debug(caplog, runner, open_changelog):
    caplog.set_level(logging.DEBUG)
    result = runner.invoke(main, ["--debug"])
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    assert "Logging level has been set to DEBUG" in caplog.text


@pytest.mark.parametrize(
    "commands",
    [["git remote add origin https://github.com/Michael-F-Bryan/auto-changelog.git"]],
)
def test_no_debug(caplog, runner, open_changelog):
    caplog.set_level(logging.DEBUG)
    result = runner.invoke(main)
    assert result.exit_code == 0, result.stderr
    assert result.output == ""
    assert "Logging level has been set to DEBUG" not in caplog.text
