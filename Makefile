

run:
	python3 AnyMate.py template.anymate

runconsole:
	python3 AnyMate.py --nogui greet template.anymate

test:
	#python2 test_AnyMate.py
	python3 test_AnyMate.py

lint:
	pylint3 AnyMate.py

linttest:
	pylint3 --no-docstring-rgx=test_* --disable=no-self-use test_*.py

pyreverse:
	pyreverse3 AnyMate.py
	dot -Tpng classes_No_Name.dot > png.png

coverage:
	python3-coverage run test_AnyMate.py
	python3-coverage report
	python3-coverage html

traces:
	python3 -m trace -t test_AnyMate.py > trace.txt
	python3 -m trace -l test_AnyMate.py > listfuncs.txt
	cat trace.txt | grep AnyMate > trace_short.txt
	python3 -m trace -t AnyMate.py --nogui greet template.anymate > nogui.txt
