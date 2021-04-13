import os
import logging
import auto_changelog
from typing import Optional

import click

from auto_changelog import generate_changelog
from auto_changelog.presenter import MarkdownPresenter, default_template
from auto_changelog.repository import GitRepository


def validate_template(ctx, param, value):

    # Check if an embedded template is passed in parameter
    if value in default_template:
        return value
    # Check if the custom template is a jinja2 file
    elif value.endswith(".jinja2"):
        return value
    else:
        raise click.BadParameter("Need to pass an embedded template name or a .jinja2 file")


@click.command()
@click.option("--gitlab", help="Set Gitlab Pattern Generation.", is_flag=True)
@click.option("--github", help="Set GitHub Pattern Generation.", is_flag=True)
@click.option(
    "-p",
    "--path-repo",
    type=click.Path(exists=True),
    default=".",
    help="Path to the repository's root directory [Default: .]",
)
@click.option("-t", "--title", default="Changelog", help="The changelog's title [Default: Changelog]")
@click.option("-d", "--description", help="Your project's description")
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="CHANGELOG.md",
    help="The place to save the generated changelog [Default: CHANGELOG.md]",
)
@click.option("-r", "--remote", default="origin", help="Specify git remote to use for links")
@click.option("-v", "--latest-version", type=str, help="use specified version as latest release")
@click.option("-u", "--unreleased", is_flag=True, default=False, help="Include section for unreleased changes")
@click.option(
    "--template",
    callback=validate_template,
    default="compact",
    help="specify template to use [compact] or a path to a custom template, default: compact ",
)
@click.option("--diff-url", default=None, help="override url for compares, use {current} and {previous} for tags")
@click.option("--issue-url", default=None, help="Override url for issues, use {id} for issue id")
@click.option(
    "--issue-pattern",
    default=r"(#([\w-]+))",
    help="Override regex pattern for issues in commit messages. Should contain two groups, original match and ID used "
    "by issue-url.",
)
@click.option(
    "--tag-pattern",
    default=None,
    help="override regex pattern for release tags. "
    "By default use semver tag names semantic. "
    "tag should be contain in one group named 'version'.",
)
@click.option("--tag-prefix", default="", help='prefix used in version tags, default: "" ')
@click.option("--stdout", is_flag=True)
@click.option("--tag-pattern", default=None, help="Override regex pattern for release tags")
@click.option("--starting-commit", help="Starting commit to use for changelog generation", default="")
@click.option("--stopping-commit", help="Stopping commit to use for changelog generation", default="HEAD")
@click.option(
    "--debug",
    is_flag=True,
    help="set logging level to DEBUG",
)
def main(
    path_repo,
    gitlab,
    github,
    title,
    description,
    output,
    remote,
    latest_version: str,
    unreleased: bool,
    template,
    diff_url,
    issue_url,
    issue_pattern,
    tag_prefix,
    stdout: bool,
    tag_pattern: Optional[str],
    starting_commit: str,
    stopping_commit: str,
    debug: bool,
):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Logging level has been set to DEBUG")

    if gitlab:
        auto_changelog.set_gitlab()

    if github:
        auto_changelog.set_github()

    # Convert the repository name to an absolute path
    repo = os.path.abspath(path_repo)

    repository = GitRepository(
        repo,
        latest_version=latest_version,
        skip_unreleased=not unreleased,
        tag_prefix=tag_prefix,
        tag_pattern=tag_pattern,
    )
    presenter = MarkdownPresenter(template=template)
    changelog = generate_changelog(
        repository,
        presenter,
        title,
        description,
        remote=remote,
        issue_pattern=issue_pattern,
        issue_url=issue_url,
        diff_url=diff_url,
        starting_commit=starting_commit,
        stopping_commit=stopping_commit,
    )

    if stdout:
        print(changelog)
    else:
        output.write(changelog)


if __name__ == "__main__":
    main()
