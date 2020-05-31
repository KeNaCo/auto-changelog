# Changelog

## 0.5.0 (2020-05-31)

#### New Features

* change how is managed compare_url feature
* add --tag-prefix, --tag-pattern and --compare-url options
* Add --tag-pattern option [#19](https://github.com/Michael-F-Bryan/auto-changelog/issues/19) (credit to @LeMimit)
#### Fixes

* test_tag_pattern works for all py versions
* change compare_url to diff_url
* take into account full specification of semver spec
* take into account prefix in tag of compare url
* fix compare url
* Git asking for username and email conf
* TypeError in CI because of PosixPath
* Handle issue pattern with one group [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Handle empty repository [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Catch missing remote [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
#### Others

* (poetry): Update dependencies in lock file
* Fix Readme contributing description
* Add support for python3.8 [#51](https://github.com/Michael-F-Bryan/auto-changelog/issues/51)
* Add integration tests for --tag-prefix --tag-pattern
* add more tests to test --compare-url option
* refactor assert condition to make it simpler
* add tests of --tag-prefix, --tag-pattern and --compare-url options
* Add --issue-pattern with invalid pattern integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --starting-commit with only one commit integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add skipping unreleased integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --stopping-commit integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --starting-commit integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --stdout integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --issue-pattern integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --issue-url integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --unreleased integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --latest-version integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --upstream integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --output integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --description integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --title integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --repo integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add --help integration test [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)
* Add integration tests [#50](https://github.com/Michael-F-Bryan/auto-changelog/issues/50)

Full set of changes: [`0.4.0...0.5.0`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.4.0...0.5.0)

## 0.4.0 (2019-10-31)

#### New Features

* (template): add release date to template
#### Fixes

* Missing {id} key in default issue template [#42](https://github.com/Michael-F-Bryan/auto-changelog/issues/42)
* Git Repo now search in parent directories [#44](https://github.com/Michael-F-Bryan/auto-changelog/issues/44)
* Missing release date in tests [#43](https://github.com/Michael-F-Bryan/auto-changelog/issues/43)
* add support of ssh configuration of the remote
* fix generation of issue url
* clean old changes
#### Refactorings

* Remove unused import from test [#43](https://github.com/Michael-F-Bryan/auto-changelog/issues/43)
#### Others

* Release of version 0.4.0
* (black): Black reformatting [#43](https://github.com/Michael-F-Bryan/auto-changelog/issues/43)
* add tests to test new generation of issue url

Full set of changes: [`0.3.0...0.4.0`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.3.0...0.4.0)

## 0.3.0 (2019-10-05)

#### New Features

* add --remote, --issue-url, --issue-pattern options, markdown links
* Latest version [#19](https://github.com/Michael-F-Bryan/auto-changelog/issues/19)
* add --starting-commit option
* add --description option
* add --title option
* add --repo option
* add --stopping-commit option
* Unreleased option implemented [#19](https://github.com/Michael-F-Bryan/auto-changelog/issues/19)
* Stdout option implemented [#19](https://github.com/Michael-F-Bryan/auto-changelog/issues/19)
* Output option implemented [#19](https://github.com/Michael-F-Bryan/auto-changelog/issues/19)
* Replace docopt with click [#19](https://github.com/Michael-F-Bryan/auto-changelog/issues/19)
* New composing/parsing algorithm
#### Fixes

* Re-fix last fix in template and tests [#40](https://github.com/Michael-F-Bryan/auto-changelog/issues/40)
* Missing empty space at the end of sections
* Remote url transformation cover all protocols ssh,git,http,https
* fix how to get url from remote
* add missing parameters
* disable file writing when stdout specified
* fix latest_version
* Use all change types in template [#24](https://github.com/Michael-F-Bryan/auto-changelog/issues/24)
#### Refactorings

* Remove unused modules and files [#17](https://github.com/Michael-F-Bryan/auto-changelog/issues/17)
* Typo in repository class name
#### Docs

* (Readme): Add gif with usage example [#21](https://github.com/Michael-F-Bryan/auto-changelog/issues/21)
* (Readme): Update Readme [#21](https://github.com/Michael-F-Bryan/auto-changelog/issues/21)
#### Others

* Release 0.3.0
* (ci): Add build and release jobs [#21](https://github.com/Michael-F-Bryan/auto-changelog/issues/21)
* Update pyproject.toml [#21](https://github.com/Michael-F-Bryan/auto-changelog/issues/21)
* Add black for formatting
* Remove docs and examples
* (poetry): Upgrade dependencies [#27](https://github.com/Michael-F-Bryan/auto-changelog/issues/27)
* Use Poetry as dependency and build managing tool [#18](https://github.com/Michael-F-Bryan/auto-changelog/issues/18)
* Set version to 1.0.0dev1 [#17](https://github.com/Michael-F-Bryan/auto-changelog/issues/17)
* (git): Replace manual gitignore with new generated one [#17](https://github.com/Michael-F-Bryan/auto-changelog/issues/17)
* (CI): Add gitlab CI support
* Reformatted by black
* Typo in docstrings
* Typo in test name
* Add pytest as testing framework

Full set of changes: [`0.1.7...0.3.0`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.7...0.3.0)

## 0.1.7 (2017-11-18)


Full set of changes: [`0.1.6...0.1.7`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.6...0.1.7)

## 0.1.6 (2017-08-09)

#### Fixes

* (template): fix tag date format
#### Docs

* Removed a space so the images are displayed correctly
* (README): Added example images to show what the script will do

Full set of changes: [`0.1.5...0.1.6`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.5...0.1.6)

## 0.1.5 (2016-07-20)

#### Fixes

* Fixed IndexError when run with no tags in the repo [[#2](https://github.com/Michael-F-Bryan/auto-changelog/issues/2)]
#### Others

* Bumped version number
* Bumping versions and trying to make PyPI installs see the template dir

Full set of changes: [`0.1.3...0.1.5`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.3...0.1.5)

## 0.1.3 (2016-07-20)

#### Others

* Bumping version numbers to make pypi install properly

Full set of changes: [`0.1.2...0.1.3`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.2...0.1.3)

## 0.1.2 (2016-07-20)

#### New Features

* Fixed setup.py so the templates are installed in the right spot
* Added an intermediate step to remove unnecessary newlines from the changelog
#### Fixes

* Fixed the issue of missing commits [[#1](https://github.com/Michael-F-Bryan/auto-changelog/issues/1)]
#### Docs

* (examples): Updated the examples with cz-cli's changelog
#### Others

* Added a requirements.txt
* Updated changelog

Full set of changes: [`0.1.1...0.1.2`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.1...0.1.2)

## 0.1.1 (2016-07-20)

#### New Features

* (template): Added "feature" group to changelog template
* Added a console script entry point, `auto-changelog`
#### Refactorings

* (templates): Refactored the templates to use a print_group() macro instead of manual copy/paste
#### Others

* Bumped the version number
* Added a changelog and makefile

Full set of changes: [`0.1.0...0.1.1`](https://github.com/Michael-F-Bryan/auto-changelog/compare/0.1.0...0.1.1)

## 0.1.0 (2016-07-20)

#### New Features

* Wrote the setup.py file
#### Docs

* (README): Added more detailed instructions to the README
* Added a README
#### Others

* Removed the Jupyter notebook stuff
* Removed the __pycache__ crap that snuck in
