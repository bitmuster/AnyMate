

run:
	python3 AnyMate.py template.anymate
test:
	python3 test_AnyMate.py
coverage:
	python3-coverage run test_AnyMate.py
	python3-coverage report
	python3-coverage html
