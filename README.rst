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

A simple example
----------------

.. image:: example-usage.gif
   :alt: Example usage of auto-changelog

Contributing
------------

To setup development environment, you may use `Poetry`_:

.. code-block:: text

    poetry install --dev

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
