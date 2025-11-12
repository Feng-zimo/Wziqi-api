# Makefile for wuziqi-api

# Python interpreter
PYTHON := python

# Project directories
SRC_DIR := Wziqi_api
TEST_DIR := tests
EXAMPLES_DIR := examples

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install      - Install the package in development mode"
	@echo "  test         - Run tests"
	@echo "  examples     - Run example scripts"
	@echo "  clean        - Clean build artifacts"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with black"
	@echo "  help         - Show this help message"

.PHONY: install
install:
	$(PYTHON) -m pip install -e .

.PHONY: test
test:
	$(PYTHON) -m pytest $(TEST_DIR) -v

.PHONY: examples
examples:
	@echo "Running basic example..."
	$(PYTHON) $(EXAMPLES_DIR)/basic_example.py
	@echo "Running advanced example..."
	$(PYTHON) $(EXAMPLES_DIR)/advanced_example.py

.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

.PHONY: lint
lint:
	$(PYTHON) -m flake8 $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)

.PHONY: format
format:
	$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)