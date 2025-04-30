# Development Guide

## Setup
1. Install dependencies:
```bash
poetry install

poetry env activate

```
2. Install pre-commit hooks:
```bash
pre-commit install
```

## Building
```bash
make package-build # Build sdist for package deployment

poetry build # Default build with *.so output
```

## Testing
```bash
nox -s test # Run tests for python versions 3.9 - 3.13

nox -s test-3.13 # Run tests for specific python version
```

## Linting
```bash
nox -s lint # cython-lint + ruff
```
## Run in dev mode

### 1. Build shared object file
```bash
poetry build
```
You can obtain .so file in `buid/lib.*`
### 2. Move .so file in `shamir_ss`
```bash
mv buid/lib.*/*.so shamir_ss/
```
### 3. Use builded package
```bash
poetry run python3 -m shamir_ss

python3 -m shamir_ss # Under activated poetry env
```

## Publishing
Publish package to PYPI using twine
```bash
make package-upload
```
> requires token configuration from pypi: `$HOME/.pypirc`
