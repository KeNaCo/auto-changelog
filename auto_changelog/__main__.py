"""
Generage a changelog straight from your git commits.

Usage: auto-changelog [options]

Options:
    -r=REPO --repo=REPO     Path to the repository's root directory [Default: .]
    -t=TITLE --title=TITLE  The changelog's title [Default: Changelog]
    -d=DESC --description=DESC
                            Your project's description
    -o=OUTFILE --output=OUTFILE
                            The place to save the generated changelog 
                            [Default: CHANGELOG.md]
    -h --help               Print this help text
    -V --version            Print the version number
"""

import os

import docopt

from auto_changelog import generate_changelog
from auto_changelog.presenter import MarkdownPresenter
from auto_changelog.repository import GitRepository
from auto_changelog import __version__


def main():
    args = docopt.docopt(__doc__, version=__version__)
    # Convert the repository name to an absolute path
    repo = os.path.abspath(args['--repo'])

    repository = GitRepository(repo)
    presenter = MarkdownPresenter()
    title = args['--title']
    description = args['--description']
    changelog = generate_changelog(repository, presenter, title, description)

    with open(args['--output'], 'w') as f:
        f.write(changelog)


if __name__ == "__main__":
    main()
