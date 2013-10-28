all: encoder

encoder: encoding.py
	python -m compileall encoding.py
	python -m compileall encoding_tests.py

test: encoding_tests.py
	python encoding_tests.py -v -x stress

stresstest: encoding_tests.py
	python encoding_tests.py -v -i stress

clean:
	rm *.pyc
