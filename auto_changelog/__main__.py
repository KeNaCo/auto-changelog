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
    -t=TEMPLATEDIR --template-dir=TEMPLATEDIR
                            The directory containing the templates used for
                            rendering the changelog 
    -c=RELEASE_COUNT --count=RELEASE_COUNT
                            How many releases to be generated from the latest
                            If 0, the whole changelog will be regenerated and the outfile will be overwritten
                            Default: 1
    -b=BRANCH --branch=BRANCH
                            Retrieve commits
                            Default: master
    -h --help               Print this help text
    -V --version            Print the version number
"""

import os
import sys

import docopt

from .parser import group_commits, traverse
from .generator import generate_changelog
from . import __version__


def main():
    args = docopt.docopt(__doc__, version=__version__)

    if args.get('--template-dir'):
        template_dir = args['--template-dir']
    else:
        # The templates are sitting at ./templates/*.jinja2
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(BASE_DIR, 'templates')

    if args.get('--count'):
        count = int(args['--count'])
    else:
        count = 1

    # Convert the repository name to an absolute path
    repo = os.path.abspath(args['--repo'])

    if args.get('--branch'):
        branch = args['--branch']
    else:
        branch = 'master'

    try:
        # Traverse the repository and group all commits to master by release
        tags, unreleased = traverse(args['--repo'], branch)
    except ValueError as e:
        print('ERROR:', e)
        sys.exit(1)
    
    changelog = generate_changelog(
            template_dir=template_dir,
            title=args['--title'],
            description=args.get('--description'),
            count=count,
            unreleased=unreleased,
            tags=tags)

    # Get rid of some of those unnecessary newlines
    # changelog = changelog.replace('\n\n\n', '\n')

    with open(args['--output'], 'w') as f:
        f.write(changelog)

if __name__ == "__main__":
    main()
