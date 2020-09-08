Auto Changelog
==============

|ci| |pypi| |version| |licence| |black|

.. |ci| image:: https://gitlab.com/KeNaCo/auto-changelog-ci-test/badges/master/pipeline.svg
   :target: https://gitlab.com/KeNaCo/auto-changelog-ci-test/commits/master
   :alt: CI Pipeline
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

or directly from source(via poetry):

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
      -r, --repo PATH            Path to the repository's root directory [Default:
                                 .]
    
      -t, --title TEXT           The changelog's title [Default: Changelog]
      -d, --description TEXT     Your project's description
      -o, --output FILENAME      The place to save the generated changelog
                                 [Default: CHANGELOG.md]
    
      -r, --remote TEXT          Specify git remote to use for links
      -v, --latest-version TEXT  use specified version as latest release
      -u, --unreleased           Include section for unreleased changes
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
      --help                     Show this message and exit.


A simple example
----------------

.. image:: example-usage.gif
   :alt: Example usage of auto-changelog

Contributing
------------

To setup development environment, you may use `Poetry`_:

.. code-block:: text

    poetry install

To activate virtualenv:

.. code-block:: text

    poetry shell

To run tests:

.. code-block:: text

    pytest

For consistent formatting, you may use `Black`_:

.. code-block:: text

    black .

.. note::

    Instead of manual run of black tool, you can consider using `Pre-commit`_.

.. _Black: https://black.readthedocs.io/en/stable/
.. _conventional style: https://www.conventionalcommits.org/en
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _Poetry: https://poetry.eustace.io/
.. _Pre-commit: https://pre-commit.com/
