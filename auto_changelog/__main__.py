import os

import click

from auto_changelog import generate_changelog
from auto_changelog.presenter import MarkdownPresenter
from auto_changelog.repository import GitRepository


@click.command()
@click.option('-o', '--output', type=click.File('w'), default='CHANGELOG.md')
@click.option('--stdout', is_flag=True)
def main(output, stdout: bool):
    # Convert the repository name to an absolute path
    repo = os.path.abspath('.')

    repository = GitRepository(repo)
    presenter = MarkdownPresenter()
    title = 'Changelog'
    description = ''
    changelog = generate_changelog(repository, presenter, title, description)
    output.write(changelog)
    if stdout:
        print(changelog)


if __name__ == "__main__":
    main()
