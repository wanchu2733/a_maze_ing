PYTHON=$(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PIP=$(if $(wildcard .venv/bin/pip),.venv/bin/pip,pip3)

activate:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip build setuptools wheel flake8 mypy

build:
	$(PYTHON) -m build --wheel

install:
	$(PIP) install dist/maze_generator-0.0.0-py3-none-any.whl

run:
	$(PYTHON) a_maze_ing.py

debug:
	$(PYTHON) -m pdb a_maze_ing.py

clean:
	rm -rf .mypy_cache __pycache__ */__pycache__ build/ dist/ *.egg-info

lint:
	$(PYTHON) -m flake8 --exclude=.venv .
	$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude build

lint-strict:
	$(PYTHON) -m flake8 --exclude=.venv .
	$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude build \
		--strict