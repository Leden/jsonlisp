setup:
	@poetry run pre-commit install

test:
	@poetry run pytest

.PHONY = setup test
