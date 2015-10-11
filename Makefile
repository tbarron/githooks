VERSION=`python githooks/__init__.py --version`

help:
	@echo "    iterate - uninstall, setup, install, test"
	@echo "    dist - setup"
	@echo "    install - pip install"
	@echo "    distclean - uninstall and remove dist"
	@echo "    clean - remove tests/__pycache__ and *.pyc"

iterate:
	pip uninstall -y githooks
	rm -rf dist
	python setup.py sdist
	pip install dist/githooks-$(VERSION).tar.gz
	py.test

dist:
	python setup.py sdist

install:
	pip install -e .

distclean:
	pip uninstall -y githooks
	rm -rf dist

clean:
	rm -rf tests/__pycache__
	find . -name "*.pyc" | xargs rm
