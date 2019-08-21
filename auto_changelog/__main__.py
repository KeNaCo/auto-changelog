import os

import click

from auto_changelog import generate_changelog
from auto_changelog.presenter import MarkdownPresenter
from auto_changelog.repository import GitRepository


@click.command()
@click.option('-r', '--repo', type=click.Path(exists=True), default='.')
@click.option('-o', '--output', type=click.File('w'), default='CHANGELOG.md')
@click.option('-u', '--unreleased', is_flag=True, default=False)
@click.option('--stdout', is_flag=True)
@click.option('--stopping-commit', help='Stopping commit to use for changelog generation', default='HEAD')
def main(repo, output, unreleased: bool, stdout: bool, stopping_commit: str):
    # Convert the repository name to an absolute path
    repo = os.path.abspath(repo)

    repository = GitRepository(repo, skip_unreleased=not unreleased)
    presenter = MarkdownPresenter()
    title = 'Changelog'
    description = ''
    changelog = generate_changelog(repository, presenter, title, description, stopping_commit=stopping_commit)
    output.write(changelog)
    if stdout:
        print(changelog)


if __name__ == "__main__":
    main()
