test:
	python -m pytest

deps:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

lint:
	@flake8 *.py app/*.py tests/*.py --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 *.py app/*.py tests/*.py --ignore=C901 --exit-zero --max-complexity=10 --max-line-length=127 --statistics

fix:
	@autopep8 --in-place *.py app/*.py tests/*.py
