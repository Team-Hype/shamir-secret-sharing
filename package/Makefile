test:
	poetry run python -m pytest

package-build:
	poetry run python setup.py build_ext --inplace

pre-commit-install:
	poetry install && poetry run pre-commit install

pre-commit-run:
	poetry run pre-commit run --all-files

pre-commit-clean:
	poetry run pre-commit clean
