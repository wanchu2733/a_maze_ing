_This project has been created as part of the 42 curriculum by wchu, ldreger._

# Description
[This project](https://projects.intra.42.fr/projects/a-maze-ing) creates a maze with an entry and exit point, finds the shortest path to the exit and displays it.

# Instructions
Please use venv in Python 3.14.0

## Makefile
This project uses a Makefile for execution. The following rules may be used:
- `build`:       Building the whl to dist folder
- `install`:     Not applicable to this project. It would install needed dependencies using `pip`.
- `run`:         Executes the program.
- `debug`:       Runs the program in debug mode using `-m pdb`.
- `clean`:       Deletes `.mypy_cache` files and `__pycache__` folders.
- `lint`:        Checks for norme compliance.
- `lint-strict`: Checks for norme compliance in strict mode.

Rules can be run by the command `make [rule]`.

# Resources
To gain an understanding of concepts such as Depth First Search, we used websites such as [GeeksforGeeks](https://www.geeksforgeeks.org/).

Generative AI (namely [Gemini](https://gemini.google.com/)) was used to gain a deeper understanding of the python syntax and python functions.

# Details


### Config File
The `config.txt` file is formatted as follows:
```bash
# Lines starting with the '#' character are ignored

# Width of maze
WIDTH=30
# Height of maze
HEIGHT=20
# Tile position of search entry (must fall within bounds)
ENTRY=12,18
# Tile position of search exit (must fall within bounds)
EXIT=2,9
# Name of the output file
OUTPUT_FILE=maze.txt
# True if there is one path to the exit, False if multiple may exist
PERFECT=True
# Seed used to generate maze layout
SEED=1
# Algorithm used to get to result
ALGORITHM=dfs
```

### Generation Algorithm
dfs. Depth-First Search (DFS) explores a maze by going as deep as possible along each path before backtracking when hitting dead ends.

prims. Randomized Prim’s generates a maze by starting at one cell and continually picking a random wall from its growing border (frontier) to carve into unvisited space, creating a natural, highly branched layout.

### Reusability
maze_generator is a standalone module able to be built to dis/maze_generator-xxx.whl and can be installed via pip install

### Project Management
Seeing that this is a group project, it was not possible for every group member to do everything.
Basic devision of tasks was for `wchu` to do the back-end (algorithms and output file generation) and for `ldreger` to handle the front-end (config passing and display logic).