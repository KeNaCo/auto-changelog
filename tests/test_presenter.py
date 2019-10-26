from datetime import date

import pytest

from auto_changelog.domain_model import Changelog, default_issue_pattern, default_tag_pattern
from auto_changelog.presenter import MarkdownPresenter


@pytest.fixture(params=["", "Title"])
def title(request):
    return request.param


@pytest.fixture(params=["", "Description"])
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
    assert empty_changelog.title in markdown
    assert empty_changelog.description in markdown


def test_markdown_presenter_changelog_with_features(changelog, markdown_presenter):
    changelog.add_release("Unreleased", date(2020, 1, 1), None)
    changelog.add_note("", "feat", "description")
    changelog.add_note("", "feat", "description", scope="scope")
    description = "{}\n\n".format(changelog.description) if changelog.description else ""
    assert_markdown = (
        "# {title}\n\n{description}## Unreleased (2020-01-01)\n\n#### New Features\n\n* description\n* (scope): description\n"
    ).format(title=changelog.title, description=description)
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown == markdown


def test_markdown_presenter_changelog_with_fixes(changelog, markdown_presenter):
    changelog.add_release("Unreleased", date(2020, 1, 1), None)
    changelog.add_note("", "fix", "description")
    changelog.add_note("", "fix", "description", scope="scope")
    description = "{}\n\n".format(changelog.description) if changelog.description else ""
    assert_markdown = (
        "# {title}\n\n{description}## Unreleased (2020-01-01)\n\n#### Fixes\n\n* description\n* (scope): description\n"
    ).format(title=changelog.title, description=description)
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown == markdown


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Some text about #42", "Some text about [#42](http://gitlab.com/issues/42)"),
        (
            "Some text with #12 and #42",
            "Some text with [#12](http://gitlab.com/issues/12) and [#42](http://gitlab.com/issues/42)",
        ),
        ("Some text will be unchanged", "Some text will be unchanged"),
        (
            "This is also valid ticket id #ACH-123",
            "This is also valid ticket id [#ACH-123](http://gitlab.com/issues/ACH-123)",
        ),
    ],
)
def test_link_default_match(text, expected, markdown_presenter):
    issue_url = "http://gitlab.com/issues/{id}"
    linked_text = markdown_presenter._link(issue_url, default_issue_pattern, text)
    assert linked_text == expected


def test_link_default_url(markdown_presenter):
    linked_text = markdown_presenter._link("", default_issue_pattern, "Some text about #42")
    assert linked_text == "Some text about #42"


@pytest.mark.parametrize("compare_url", ["https://github.com/LeMimit/auto-changelog/compare/{previous}...{current}"])
@pytest.mark.parametrize(
    "text, prefix, expected",
    [
        ("## 0.3.0", "", "## 0.3.0"),
        (
            "## 0.3.0 \n## 0.1.7",
            "",
            "## [0.3.0](https://github.com/LeMimit/auto-changelog/compare/0.1.7...0.3.0) \n## 0.1.7",
        ),
        (
            "## 0.3.0 \n## 1.0.0-alpha",
            "",
            "## [0.3.0](https://github.com/LeMimit/auto-changelog/compare/1.0.0-alpha...0.3.0) \n## 1.0.0-alpha",
        ),
        (
            "# 0.3.0 \n# 0.1.7",
            "",
            "# [0.3.0](https://github.com/LeMimit/auto-changelog/compare/0.1.7...0.3.0) \n# 0.1.7",
        ),
        (
            "### 0.3.0 \n### 0.1.7",
            "",
            "### [0.3.0](https://github.com/LeMimit/auto-changelog/compare/0.1.7...0.3.0) \n### 0.1.7",
        ),
        (
            "## 0.3.0 \n## 0.1.7\n## 0.1.1",
            "",
            "## [0.3.0](https://github.com/LeMimit/auto-changelog/compare/0.1.7...0.3.0)"
            " \n## [0.1.7](https://github.com/LeMimit/auto-changelog/compare/0.1.1...0.1.7)\n## 0.1.1",
        ),
        (
            "## 0.3.0 \n## 1.2.3-SNAPSHOT-123\n## 1.0.0-rc.1+build.1",
            "",
            "## [0.3.0](https://github.com/LeMimit/auto-changelog/compare/1.2.3-SNAPSHOT-123...0.3.0)"
            " \n## [1.2.3-SNAPSHOT-123](https://github.com/LeMimit/auto-changelog/compare/1.0.0-rc.1+build.1...1.2.3-SNAPSHOT-123)"
            "\n## 1.0.0-rc.1+build.1",
        ),
        ("## 0.3.0 \n## 0.1.7", "v", "## 0.3.0 \n## 0.1.7"),
        (
            "## v0.3.0 \n## v0.1.7",
            "v",
            "## [v0.3.0](https://github.com/LeMimit/auto-changelog/compare/v0.1.7...v0.3.0) \n## v0.1.7",
        ),
        (
            "## v0.3.0 \n## v0.1.7\n## v0.1.1",
            "v",
            "## [v0.3.0](https://github.com/LeMimit/auto-changelog/compare/v0.1.7...v0.3.0)"
            " \n## [v0.1.7](https://github.com/LeMimit/auto-changelog/compare/v0.1.1...v0.1.7)\n## v0.1.1",
        ),
        (
            "## v0.3.0 \n## v1.2.3-SNAPSHOT-123\n## v1.0.0-rc.1+build.1",
            "v",
            "## [v0.3.0](https://github.com/LeMimit/auto-changelog/compare/v1.2.3-SNAPSHOT-123...v0.3.0)"
            " \n## [v1.2.3-SNAPSHOT-123](https://github.com/LeMimit/auto-changelog/compare/v1.0.0-rc.1+build.1...v1.2.3-SNAPSHOT-123)"
            "\n## v1.0.0-rc.1+build.1",
        ),
    ],
)
def test_compare_default_match(compare_url, text, prefix, expected, markdown_presenter):
    linked_text = markdown_presenter._title(compare_url, default_tag_pattern, prefix, text)
    assert linked_text == expected


@pytest.mark.parametrize("compare_url", ["https://github.com/LeMimit/auto-changelog/compare/{previous}...{current}"])
@pytest.mark.parametrize(
    "text, tag_pattern, prefix, expected",
    [
        ("## 0.3.0", "(?P<version>[1-9])", "", "## 0.3.0"),
        ("## 3", "(?P<version>[1-9])", "", "## 3"),
        ("## 3", "([1-9])", "", "## 3"),
        ("## 0.3.0 \n## 0.1.7", "(?P<version>[1-9])", "", "## 0.3.0 \n## 0.1.7"),
        (
            "## 3 \n## 2",
            "(?P<version>[1-9])",
            "",
            "## [3](https://github.com/LeMimit/auto-changelog/compare/2...3) \n## 2",
        ),
        ("# 3 \n# 2", "(?P<version>[1-9])", "", "# [3](https://github.com/LeMimit/auto-changelog/compare/2...3) \n# 2"),
        ("## 3 \n## 2", "([1-9])", "", "## 3 \n## 2"),
        ("## 0.3.0 \n## 0.1.7\n## 0.1.1", "(?P<version>[1-9])", "", "## 0.3.0 \n## 0.1.7\n## 0.1.1"),
        (
            "## 3 \n## 2\n## 1",
            "(?P<version>[1-9])",
            "",
            "## [3](https://github.com/LeMimit/auto-changelog/compare/2...3)"
            " \n## [2](https://github.com/LeMimit/auto-changelog/compare/1...2)\n## 1",
        ),
        ("## 3 \n## 2\n## 1", "([1-9])", "", "## 3 \n## 2\n## 1"),
        (
            "# 3 \n# 2\n# 1",
            "(?P<version>[1-9])",
            "",
            "# [3](https://github.com/LeMimit/auto-changelog/compare/2...3)"
            " \n# [2](https://github.com/LeMimit/auto-changelog/compare/1...2)\n# 1",
        ),
        ("## v3 \n## v2\n## v1", "([1-9])", "v", "## v3 \n## v2\n## v1"),
        (
                "# v3 \n# v2\n# v1",
                "(?P<version>[1-9])",
                "v",
                "# [v3](https://github.com/LeMimit/auto-changelog/compare/v2...v3)"
                " \n# [v2](https://github.com/LeMimit/auto-changelog/compare/v1...v2)\n# v1",
        )
    ],
)
def test_compare_custom_match(compare_url, text, tag_pattern, prefix, expected, markdown_presenter):
    linked_text = markdown_presenter._title(compare_url, tag_pattern, prefix, text)
    assert linked_text == expected
