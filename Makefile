.PHONY: install run test lint format typecheck evaluation check

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

evaluation:
	python pipelines/evaluation/evaluate.py

check: lint format-check typecheck test evaluation

format-check:
	ruff format --check app tests pipelines serving
