PYTHON=`which python3`
PIP=`which pip3`

.PHONY: clean clear cls
clean clear cls::
	find . -name '*.pyc' -delete
	find . -type d | grep _pycache_ | xargs rm -rf
	find . -type d -name '.tox' -exec rm -fr {} +
	find . -name 'report.xml' -exec rm -f {} +
	rm -rf .coverage
	rm -rf htmlcov
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find ../ -type f -name .terraform.lock.hcl -exec rm -f {} +
	find ../ -type d -name .terraform -exec rm -rf {} +
	find ../ -type f -name output.xml -exec rm -f {} +
	find ../ -type d -name build -exec rm -rf {} +

.PHONY: cleanse
cleanse:: clean
	find ../ -type d -name .centralized-makefile -exec rm -rf {} +
	find ../ -type d -name venv -exec rm -rf {} +
