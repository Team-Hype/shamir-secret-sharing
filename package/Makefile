
.PHONY: package-build
package-build:
	poetry build -f sdist
	poetry run twine check dist/*

.PHONY: package-upload
package-upload: package-build
	poetry run twine upload dist/*.tar.gz

.PHONY: pre-commit-install
pre-commit-install:
	poetry install && poetry run pre-commit install

.PHONY: pre-commit-run
pre-commit-run:
	poetry run pre-commit run --all-files

.PHONY: pre-commit-clean
pre-commit-clean:
	poetry run pre-commit clean


TARGET_VERSION=3.13
.PHONY: nox
nox:
	poetry run python3 -m nox -s lint test-$(TARGET_VERSION)

.PHONY: test
test:
	poetry run python3 -m nox -s test

.PHONY: clean
clean:
	@rm -rf build/ dist/ .mypy_cache/ .pytest_cache/ shares/
	@rm -rf shamir_ss.egg-info/ __pycache__/ .nox/
	@rm -f shamir_ss/*.so shamir_ss/*.c
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: tag
tag:
	git tag v$(shell poetry version -s)
	git push origin --tags
