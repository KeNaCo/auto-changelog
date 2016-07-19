# Changelog
## [Unreleased]


### Administration and Chores
- [package] update babel-cli to version 6.10.1 (#254)
- [package] update nyc to version 6.6.1 (#258)
- [package] update proxyquire to version 1.7.9 (#228)
- [package] update ghooks to version 1.2.4 (#259)
- [package] update glob to version 7.0.4 (#260)
- [package] update nodemon to version 1.9.2 (#214)
- save npm dependencies with pinned version by default (#261)
- avoid build run-scripts on local npm install (#255)
- [package] update glob to version 7.0.5 (#263)
- [package] update semver to version 5.1.1 (#265)
- [package] update find-node-modules to version 1.0.3 (#270)
- [package] update semver to version 5.2.0 (#271)
- [package] update proxyquire to version 1.7.10 (#272)
- [package] update ghooks to version 1.3.0 (#274)
- [package] update inquirer to version 1.1.1 (#278)
- [package] update inquirer to version 1.1.2 (#280)
- [package] update axios to version 0.13.0 (#282)
- [package] update semver to version 5.3.0 (#283)
- [package] update axios to version 0.13.1 (#284)


## v2.8.2 (2016-25-03)
### Bug Fixes
- [package] add supported engines to package specification (#229)


### Documentation Changes
- [usage] conventional commit messages as a global utility (#209)
### Administration and Chores
- [package] update gulp-git to version 1.7.2 (#239)
- [package] update mocha to version 2.5.2 (#244)
- [package] update inquirer to version 1.0.3 (#247)
- [package] update axios to version 0.12.0 (#248)


## v2.8.1 (2016-39-25)
### Bug Fixes
- [package] update cz-conventional-changelog to version 1.1.6 (#206)


## v2.8.0 (2016-33-20)
### Bug Fixes
- [dependencies] Update dependencies.


### Documentation Changes
- [bootstrap] add documentation for passing config via bootstrap (#195)

## v2.7.6 (2016-50-31)
### Bug Fixes
- [commit] does not try to escape backticks on Windows


## v2.7.5 (2016-36-31)
### Bug Fixes
- [commit] allow backticks in commit message


## v2.7.4 (2016-34-30)
### Bug Fixes
- [commit] allow quotes in commit message


## v2.7.3 (2016-06-18)
### Bug Fixes
- [lib] keep newline at the end of package.json


### Documentation Changes
- [retry] Updated docs to show ways to run --retry

## v2.7.2 (2016-15-11)
### Bug Fixes
- [lib] Expose commitizen as a library


### Documentation Changes
- [retry] add documentation for retry command

## v2.7.1 (2016-07-11)
### Bug Fixes
- [cache] use lodash assign for better node 0.12 support


## v2.7.0 (2016-50-11)

### New Features
- [commit] add --retry option



## v2.6.3 (2016-17-09)
### Bug Fixes
- [commit] fix commit to allow --verbose flag


## v2.6.2 (2016-50-09)
### Bug Fixes
- [testing] update babel and code coverage


## v2.6.1 (2016-43-04)
### Bug Fixes
- make gulp depedencies available for prod installs


## v2.6.0 (2016-20-04)

### New Features
- [adapter] support npm module names in commitizen.path config



## v2.5.1 (2016-50-03)
### Bug Fixes
- [dependencies] update many dependencies


### Documentation Changes
- [cli] Rename reference to czConfig
### Administration and Chores
- [dependencies] move dependencies to devDependencies where possible


## v2.5.0 (2016-49-10)

### New Features
- [commit] allow override options passed to git commit

### Documentation Changes
- [readme] Adds semantic-release badge
### Administration and Chores
- [dependencies] upgrade dependencies


## v2.4.6 (2015-21-18)
### Bug Fixes
- [commit] fixes Windows multiline commits

### Administration and Chores
- [tests] fixes OS-based difference in git log output


## v2.4.5 (2015-03-17)
### Bug Fixes
- [adapter] fix package.json spaces being removed


### Documentation Changes
- [readme] commitizen init wording changes
### Administration and Chores
- [tests] adds appveyor test config
- [tests] remove node 0.10 from tests config
- [tests] add appveyor.yml
- [tests] add appveyor artifacts
- [tests] push test artifacts to appveyor
- [tests] use on_finish to always keep appveyor artifacts


## v2.4.4 (2015-30-09)
### Bug Fixes
- [dependencies] fix lodash is missing bug


## v2.4.3 (2015-26-09)
### Bug Fixes
- [dependencies] updates chai and dedent depedencies


## v2.4.2 (2015-46-09)
### Bug Fixes
- [adapter] fix windows json editing


## v2.4.1 (2015-56-03)
### Bug Fixes
- [config] fixes incorrect deprecation notice

### Administration and Chores
- [package] update nodemon to version 1.8.1


## v2.4.0 (2015-03-01)

### New Features
- [compile] Rebuild package on file change in dev-mode

### Refactoring
- [util] Moved util.js in to the src folder


### Administration and Chores
- [deps] upgrade to inquirer 0.11.0
- [package] update nodemon to version 1.8.0


## v2.3.0 (2015-32-23)

### New Features
- [config] use npm config object, deprecate czConfig



## v2.2.1 (2015-13-22)
### Bug Fixes
- [cli] Use only file names when determining if the staging area is clean

### Administration and Chores
- [build] only build master 🏢


## v2.2.0 (2015-49-22)

### New Features
- [commit] enable githook output streaming

### Documentation Changes
- [readme] add badges to readme
### Administration and Chores
- [build] Add ghooks and pre-commit test hook
- [package] update nodemon to version 1.7.2


## v2.1.0 (2015-02-17)
### Bug Fixes
- [parser] fix json parse dependency
- [build] fixes the travisCI build config

### Administration and Chores
- [releasing] Add travis config, semantic-release


## Version 2.0.2 (2015-22-16)
### Bug Fixes
- [cli] adds babel/register ignore overrides


## Version 2.0.1 (2015-25-16)
### Bug Fixes
- [cli] fix babel import errors


## Version 2.0 (2015-05-16)

### Refactoring
- [cli] Completely rewrite commitizen

### Documentation Changes
- [readme] add alternate czconfig info

## Version 1.0.5 (2015-29-28)

### Documentation Changes
- [readme] Add link to validate-commit-msg
### Administration and Chores
- [package] updated inquirer to version 0.10.1


## Version 1.0.4 (2015-23-08)

### New Features
- [cli] Create initial commit
### Bug Fixes
- [wrapping] Fix fields to wrap instead of truncate at 100 characters


### Documentation Changes
- [cli] Add initial readme based docs
- [cli] Add screenshot of add-commit

