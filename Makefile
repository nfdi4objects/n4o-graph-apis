deps: .venv
.venv: requirements.txt requirements-dev.txt
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements-dev.txt

test:
	@. .venv/bin/activate && coverage run -m pytest -v -s && coverage report -m

dev:
	.venv/bin/python app.py --debug

lint: 
	@.venv/bin/flake8 *.py lib/*.py tests/*.py --select=E9,F63,F7,F82 --show-source --statistics
	@.venv/bin/flake8 *.py lib/*.py tests/*.py --ignore=C901 --exit-zero --max-complexity=10 --max-line-length=127 --statistics

fix:
	@.venv/bin/autopep8 --in-place *.py lib/*.py tests/*.py

docker:
	@docker build -t n4o-graph-apis .
