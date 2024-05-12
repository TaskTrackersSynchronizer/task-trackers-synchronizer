.PHONY: lint test autopep8

all: lint test

lint:
	poetry run flake8 app

test:
	poetry run pytest tests/

autopep8:
	poetry run autopep8 -r -i app
