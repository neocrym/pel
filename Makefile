help:
	echo HELP
.PHONY: help

fmt:
	@echo "Running black formatter"
	poetry run black pel
	@echo "Running isort formatter"
	poetry run isort pel
.PHONY: fmt

pylint: fmt
	@echo "Running pylint linter"
	poetry run pylint pel
.PHONY: pylint

mypy: fmt
	@echo "Running mypy linter"
	poetry run mypy pel
.PHONY: mypy

lint: pylint mypy
.PHONY: lint

pyinstaller:
	poetry run pyinstaller --name=pel --onefile --clean --noconfirm pel/console.py
.PHONY: pyinstaller

vendor:
	poetry run python-vendorize
.PHONY: vendor