Auto Changelog
==============

|actions| |ci| |pypi| |version| |licence| |black|

.. |ci| image:: https://gitlab.com/KeNaCo/auto-changelog/badges/master/pipeline.svg
   :target: https://gitlab.com/KeNaCo/auto-changelog/-/commits/master
   :alt: Gitlab CI
.. |actions| image:: https://github.com/KeNaCo/auto-changelog/actions/workflows/ci.yml/badge.svg?branch=master
   :target: https://github.com/KeNaCo/auto-changelog/actions/workflows/ci.yml
   :alt: Github Actions
.. |pypi| image:: https://img.shields.io/pypi/v/auto-changelog
   :target: https://pypi.org/project/auto-changelog/
   :alt: PyPI
.. |version| image:: https://img.shields.io/pypi/pyversions/auto-changelog
   :alt: PyPI - Python Version
.. |licence| image:: https://img.shields.io/pypi/l/auto-changelog
   :alt: PyPI - License
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code style - Black

A quick script that will generate a changelog for any git repository using `conventional style`_ commit messages.

Installation
------------

Install and update using `pip`_:

.. code-block:: text

    pip install auto-changelog

or directly from source(via `Poetry`_):

.. code-block:: text

    poetry install
    poetry build
    pip install dist/*.whl

Usage
-----
You can list the command line options by running `auto-changelog --help`:

.. code-block:: text

    Usage: auto-changelog [OPTIONS]

    Options:
      -p, --path-repo PATH       Path to the repository's root directory
                                 [Default: .]

      -t, --title TEXT           The changelog's title [Default: Changelog]
      -d, --description TEXT     Your project's description
      -o, --output FILENAME      The place to save the generated changelog
                                 [Default: CHANGELOG.md]

      -r, --remote TEXT          Specify git remote to use for links
      -v, --latest-version TEXT  use specified version as latest release
      -u, --unreleased           Include section for unreleased changes
      --template TEXT            specify template to use [compact] or a path to a
                                 custom template, default: compact

      --diff-url TEXT            override url for compares, use {current} and
                                 {previous} for tags

      --issue-url TEXT           Override url for issues, use {id} for issue id
      --issue-pattern TEXT       Override regex pattern for issues in commit
                                 messages. Should contain two groups, original
                                 match and ID used by issue-url.

      --tag-pattern TEXT         override regex pattern for release tags. By
                                 default use semver tag names semantic. tag should
                                 be contain in one group named 'version'.

      --tag-prefix TEXT          prefix used in version tags, default: ""
      --stdout
      --tag-pattern TEXT         Override regex pattern for release tags
      --starting-commit TEXT     Starting commit to use for changelog generation
      --stopping-commit TEXT     Stopping commit to use for changelog generation
      --debug                    set logging level to DEBUG
      --help                     Show this message and exit.


A simple example
----------------

.. image:: example-usage.gif
   :alt: Example usage of auto-changelog

Contributing
------------

To setup development environment, you may use `Poetry`_.
These instructions will assume that you have already `Poetry`_ as well as GNU make locally installed
on your development computer.

These instructions will assume that you have already poetry (https://python-poetry.org/) locally installed
on your development computer.

1. Fork the `auto-changelog` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/auto-changelog.git

3. Initialize your local development environment of auto-changelog.
   This will include creating a virtualenv using poetry, installing dependencies and registering git hooks
   using pre-commit::

    $ cd auto-changelog/
    $ make init-dev

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass linting, formating, and the
   tests, including testing other Python versions with tox::

    $ make lint         # check style with flake8
    $ make format       # run autoformat with isort and black
    $ make test         # run tests quickly with the default Python
    $ make test-all     # run tests on every Python version with tox


6. Commit your changes and push your branch to GitHub. Upon commit pre-commit will automatically run
   flake8 and black and report if changes have been made or need to be fixed by you::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.



.. _Black: https://black.readthedocs.io/en/stable/
.. _conventional style: https://www.conventionalcommits.org/en
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _Poetry: https://poetry.eustace.io/
.. _Pre-commit: https://pre-commit.com/
