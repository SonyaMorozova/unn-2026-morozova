
PYTHON ?= python3

.PHONY: install test ruff-cs-check ruff-cs-fix ruff-linter-check ruff-linter-fix mypy-check check build

install:
	$(PYTHON) -m pip install ruff mypy

test:
	$(PYTHON) -m unittest discover -s tests -v

ruff-cs-check:
	$(PYTHON) -m ruff format --check .

ruff-cs-fix:
	$(PYTHON) -m ruff format .

ruff-linter-check:
	$(PYTHON) -m ruff check .

ruff-linter-fix:
	$(PYTHON) -m ruff check --fix .

mypy-check:
	$(PYTHON) -m mypy bot

check: ruff-cs-check ruff-linter-check mypy-check test

build:
	docker build -t unn-2026-morozova:latest .
