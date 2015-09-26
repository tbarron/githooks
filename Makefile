VERSION=`python githooks/__init__.py --version`

iterate:
	pip uninstall -y githooks
	rm -rf dist
	python setup.py sdist
	pip install dist/githooks-$(VERSION).tar.gz
	py.test

dist:
	python setup.py sdist

install:
	pip install dist/githooks-2015.0119.14.tar.gz

clean:
	pip uninstall -y githooks
	rm -rf dist
