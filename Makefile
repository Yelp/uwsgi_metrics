.PHONY: docs test clean

test:
	tox

docs:
	tox -e docs

clean:
	find . -name '*.pyc' -delete
	rm -rf uWSGI_Metrics.egg-info
	rm -rf .tox
	rm -f MANIFEST
