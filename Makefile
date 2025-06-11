init:
	python -m pip install -r requirements.txt

flake8:
	python -m flake8 src/ecommerce_api_wrapper

publish:
	python -m pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info
