import os

import click

from auto_changelog import generate_changelog
from auto_changelog.presenter import MarkdownPresenter
from auto_changelog.repository import GitRepository


@click.command()
@click.option(
    "-r",
    "--repo",
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
@click.option("--issue-url", default=None, help="Override url for issues, use {id} for issue id")
@click.option(
    "--issue-pattern",
    default=r"(#([\w-]+))",
    help="Override regex pattern for issues in commit messages. Should contain two groups, original match and ID used by issue-url.",
)
@click.option("--stdout", is_flag=True)
@click.option("--starting-commit", help="Starting commit to use for changelog generation", default="")
@click.option("--stopping-commit", help="Stopping commit to use for changelog generation", default="HEAD")
def main(
    repo,
    title,
    description,
    output,
    remote,
    latest_version: str,
    unreleased: bool,
    issue_url,
    issue_pattern,
    stdout: bool,
    starting_commit: str,
    stopping_commit: str,
):
    # Convert the repository name to an absolute path
    repo = os.path.abspath(repo)

    repository = GitRepository(repo, latest_version=latest_version, skip_unreleased=not unreleased)
    presenter = MarkdownPresenter()
    changelog = generate_changelog(
        repository,
        presenter,
        title,
        description,
        remote=remote,
        issue_pattern=issue_pattern,
        issue_url=issue_url,
        starting_commit=starting_commit,
        stopping_commit=stopping_commit,
    )

    if stdout:
        print(changelog)
    else:
        output.write(changelog)


if __name__ == "__main__":
    main()
