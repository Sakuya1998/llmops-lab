.PHONY: install run test lint format typecheck check

install:
	python -m pip install -e ".[dev]"

run:
	uvicorn model_ops_api.main:app --reload --app-dir app

test:
	pytest

lint:
	ruff check .

format:
	ruff format app tests pipelines serving

typecheck:
	mypy app

check: lint format-check typecheck test

format-check:
	ruff format --check app tests pipelines serving
