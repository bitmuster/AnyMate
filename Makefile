

run:
	python3 AnyMate.py template.anymate

test:
	#python2 test_AnyMate.py
	python3 test_AnyMate.py

lint:
	pylint3 *.py 

coverage:
	python3-coverage run test_AnyMate.py
	python3-coverage report
	python3-coverage html
