activate:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip build setuptools wheel

build:
	.venv/bin/python -m build --wheel

install:
	.venv/bin/pip install dist/maze_generator-0.0.0-py3-none-any.whl

run:
	.venv/bin/python a_maze_ing.py

debug:
	.venv/bin/python -m pdb a_maze_ing.py

clean:
	rm -rf .mypy_cache
	rm -rf */__pycache__

lint:
	flake8 --exclude=.venv .
	.venv/bin/python -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 --exclude=.venv .
	.venv/bin/python -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--strict