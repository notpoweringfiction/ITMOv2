.PHONY: test unit e2e

PYTHON ?= python3
PROJ_ROOT := $(abspath $(CURDIR)/../../..)

unit:
	PYTHONPATH=$(PROJ_ROOT) $(PYTHON) -m unittest -v practices.practice_05.hw5.tests.test_logic

e2e:
	PYTHONPATH=$(PROJ_ROOT) $(PYTHON) -m unittest -v practices.practice_05.hw5.tests.test_cli

test: unit e2e
