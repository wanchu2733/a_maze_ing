install:
	pip install maze_generator-0.0.0.whl

run:
	python3 a_maze_ing.py

debug:
	python3 -m pdb a_maze_ing.py

clean:
	rm -rf .mypy_cache
	rm -rf */__pycache__

lint:
	flake8 --exclude=.venv .
	python3 -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 --exclude=.venv .
	python3 -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--strict