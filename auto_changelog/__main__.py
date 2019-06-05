import os

import click

from auto_changelog import generate_changelog
from auto_changelog.presenter import MarkdownPresenter
from auto_changelog.repository import GitRepository


def main():
    # Convert the repository name to an absolute path
    repo = os.path.abspath('.')

    repository = GitRepository(repo)
    presenter = MarkdownPresenter()
    title = 'Changelog'
    description = ''
    changelog = generate_changelog(repository, presenter, title, description)


if __name__ == "__main__":
    main()
