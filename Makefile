.PHONY: docs test clean

test:
	tox

docs:
	tox -e docs

clean:
	git clean -Xfd
