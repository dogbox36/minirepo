.PHONY: install test lint clean report

install:
	pip install -e .[dev]

test:
	pytest

test-smoke:
	pytest -m smoke

test-regression:
	pytest -m regression

lint:
	ruff check .
	black --check .
	mypy src tests

format:
	ruff check --fix .
	black .

clean:
	rm -rf .pytest_cache
	rm -rf .artifacts/*
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
