help:
	echo HELP
.PHONY: help

install:
	poetry install --no-dev --remove-untracked
.PHONY: install

install-dev:
	poetry install --remove-untracked
.PHONY: install-dev

fmt:
	@echo "Running black formatter"
	poetry run black pel tests
	@echo "Running isort formatter"
	poetry run isort pel tests
.PHONY: fmt

fmt-check:
	poetry run black --check pel tests
	poetry run isort --check pel tests
.PHONY: fmt-check

pylint: fmt
	@echo "Running pylint linter"
	poetry run pylint pel tests
.PHONY: pylint

mypy: fmt
	@echo "Running mypy linter"
	poetry run mypy pel tests
.PHONY: mypy

lint: pylint mypy
.PHONY: lint

pyinstaller:
	poetry run pyinstaller --name=pel --onefile --clean --noconfirm pel/console.py
.PHONY: pyinstaller

test:
	poetry run pytest
.PHONY: test

vendor:
	poetry run python-vendorize
.PHONY: vendor