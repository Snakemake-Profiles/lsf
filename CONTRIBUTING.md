# Contributing

Contributions are always very welcome.

[TOC]:#

# Table of Contents
- [Install](#install)
- [Tests](#tests)
- [Formatting](#formatting)
- [Linting](#linting)



We suggest you fork this repository, make the changes on your fork, and then put in a
**pull request to the `development` branch.**

## Install

You can find the dependencies in `requirements.txt` and `dev-requirements.txt`. They can
be installed with

```shell
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

## Tests

Make sure the test suite passes before pushing any code. If you add any code, then please provide
tests that cover all of the code added. The test suite can be run with coverage

```shell
cd tests
pytest --cov=./
```

## Formatting

Please format code with [`black`][black] (default settings) before pushing.

```shell
black .
```

## Linting

Ensure there are no `flake8` errors before pushing.

```shell
flake8 --count .
```

Please make sure you use [type annotations][types] for function parameters and return types.

[black]: https://github.com/psf/black
[types]: https://www.python.org/dev/peps/pep-0484/

