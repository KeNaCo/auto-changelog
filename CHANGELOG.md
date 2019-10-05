# Changelog

## 0.3.0

#### New Features

* add --remote, --issue-url, --issue-pattern options, markdown links
* Latest version [#19](https://github.com/KeNaCo/issues)
* add --starting-commit option
* add --description option
* add --title option
* add --repo option
* add --stopping-commit option
* Unreleased option implemented [#19](https://github.com/KeNaCo/issues)
* Stdout option implemented [#19](https://github.com/KeNaCo/issues)
* Output option implemented [#19](https://github.com/KeNaCo/issues)
* Replace docopt with click [#19](https://github.com/KeNaCo/issues)
* New composing/parsing algorithm
#### Fixes

* Re-fix last fix in template and tests [#40](https://github.com/KeNaCo/issues)
* Missing empty space at the end of sections
* Remote url transformation cover all protocols ssh,git,http,https
* fix how to get url from remote
* add missing parameters
* disable file writing when stdout specified
* fix latest_version
* Use all change types in template [#24](https://github.com/KeNaCo/issues)
#### Refactorings

* Remove unused modules and files [#17](https://github.com/KeNaCo/issues)
* Typo in repository class name
#### Docs

* (Readme): Add gif with usage example [#21](https://github.com/KeNaCo/issues)
* (Readme): Update Readme [#21](https://github.com/KeNaCo/issues)
#### Others

* (ci): Add build and release jobs [#21](https://github.com/KeNaCo/issues)
* Update pyproject.toml [#21](https://github.com/KeNaCo/issues)
* Add black for formatting
* Remove docs and examples
* (poetry): Upgrade dependencies [#27](https://github.com/KeNaCo/issues)
* Use Poetry as dependency and build managing tool [#18](https://github.com/KeNaCo/issues)
* Set version to 1.0.0dev1 [#17](https://github.com/KeNaCo/issues)
* (git): Replace manual gitignore with new generated one [#17](https://github.com/KeNaCo/issues)
* (CI): Add gitlab CI support
* Reformatted by black
* Typo in docstrings
* Typo in test name
* Add pytest as testing framework

## 0.1.7


## 0.1.6

#### Fixes

* (template): fix tag date format
#### Docs

* Removed a space so the images are displayed correctly
* (README): Added example images to show what the script will do

## 0.1.5

#### Fixes

* Fixed IndexError when run with no tags in the repo [[#2](https://github.com/KeNaCo/issues)]
#### Others

* Bumped version number
* Bumping versions and trying to make PyPI installs see the template dir

## 0.1.3

#### Others

* Bumping version numbers to make pypi install properly

## 0.1.2

#### New Features

* Fixed setup.py so the templates are installed in the right spot
* Added an intermediate step to remove unnecessary newlines from the changelog
#### Fixes

* Fixed the issue of missing commits [[#1](https://github.com/KeNaCo/issues)]
#### Docs

* (examples): Updated the examples with cz-cli's changelog
#### Others

* Added a requirements.txt
* Updated changelog

## 0.1.1

#### New Features

* (template): Added "feature" group to changelog template
* Added a console script entry point, `auto-changelog`
#### Refactorings

* (templates): Refactored the templates to use a print_group() macro instead of manual copy/paste
#### Others

* Bumped the version number
* Added a changelog and makefile

## 0.1.0

#### New Features

* Wrote the setup.py file
#### Docs

* (README): Added more detailed instructions to the README
* Added a README
#### Others

* Removed the Jupyter notebook stuff
* Removed the __pycache__ crap that snuck in
