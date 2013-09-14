PYTHON=PYTHONPATH="$(shell pwd)" python
TESTIFY=$(PYTHON) "$(shell which testify)"

.PHONY: test

tests: test

test:
	$(TESTIFY) tests
