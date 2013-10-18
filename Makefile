.PHONY: test clean

test:
	tox

clean:
	find . -name '*.pyc' -delete
	rm -rf uWSGI_Metrics.egg-info
	rm -rf .tox
	rm -f MANIFEST
