PYTHON = python3
PROJECT = auto_changelog
DESCRIPTION = 'A quick script that will generate a changelog for any git \
			  repository using "conventional style" commit messages.'

changes:
	$(PYTHON) -m $(PROJECT) --description $(DESCRIPTION)


.PHONY: changes
