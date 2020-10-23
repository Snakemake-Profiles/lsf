COVG_REPORT = tests/htmlcov/index.html
OS := $(shell uname -s)
BOLD := $(shell tput bold)
NORMAL := $(shell tput sgr0)

.PHONY: install-ci
install-ci:
	  python -m pip install --upgrade pip
	  python -m pip install -r requirements.txt
	  python -m pip install --pre -r dev-requirements.txt

.PHONY: lint
lint:
	flake8 .

# TEST ########################################################################
.PHONY: test
test:
	cd tests/ && pytest --cov=src --cov-branch --cov-report=html --cov-report=term && cd ..

.PHONY: test-ci
test-ci:
	cd tests/ && pytest --cov=src --cov-branch --cov-report=xml --cov-report=term && cd ..

.PHONY: coverage
coverage: test
ifeq ($(OS), Linux)
	xdg-open $(COVG_REPORT)
else ifeq ($(OS), Darwin)
	open $(COVG_REPORT)
else
	echo "ERROR: Unknown OS detected - $OS"
endif

