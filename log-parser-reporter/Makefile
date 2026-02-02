.PHONY: install test lint clean report-sample

install:
	pip install -e .[dev]

test:
	pytest

lint:
	ruff check .
	black --check .
	mypy src tests

format:
	ruff check --fix .
	black .

clean:
	rm -rf .pytest_cache
	rm -rf out
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
