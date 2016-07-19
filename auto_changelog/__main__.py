"""
Generage a changelog straight from your git commits.

Usage: gen-changelog [options]

Options:
    -r=REPO --repo=REPO     Path to the repository's root directory [Default: .]
    -t=TITLE --title=TITLE  The changelog's title [Default: Changelog]
    -d=DESC --description=DESC
                            Your project's description
    -o=OUTFILE --output=OUTFILE
                            The place to save the generated changelog 
                            [Default: CHANGELOG.md]
    -t=TEMPLATEDIR --template-dir=TEMPLATEDIR
                            The directory containing the templates used for
                            rendering the changelog 
    -h --help               Print this help text
    -V --version            Print the version number
"""

__version__ = '0.1.0'

import os
import sys

import docopt

from .parser import group_commits, traverse
from .generator import generate_changelog


def main(args):
    if args.get('--template-dir'):
        template_dir = args['--template-dir']
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir = os.path.join(BASE_DIR, 'templates')

    # Convert the repository name to an absolute path
    repo = os.path.abspath(args['--repo'])

    # Traverse the repository and group all commits to master by release
    tags, unreleased = traverse(args['--repo'])

    changelog = generate_changelog(
            template_dir=template_dir,
            title=args['--title'],
            description=args.get('--description'),
            unreleased=unreleased,
            tags=tags)

    with open(args['--output'], 'w') as f:
        f.write(changelog)

if __name__ == "__main__":
    args = docopt.docopt(__doc__, version=__version__)
    main(args)
