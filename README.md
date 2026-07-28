_This project has been created as part of the 42 curriculum by wchu, ldreger._

# Description
[This project](https://projects.intra.42.fr/projects/a-maze-ing) creates a maze with an entry and exit point, finds the shortest path to the exit and displays it. Re-generation, toggling shortest path visibility, color options, and animation speed can be set using a CLI menu.

# Instructions
The program can be run using `python3 a_maze_ing.py [FILE]`, where `[FILE]` is the configuration file (see [Config File](#config-file)). When using the Makefile, the recognized file name is `config.txt`.

## Makefile
This project uses a Makefile for execution. The following rules may be used:
- `run`:         Executes the program.
- `debug`:       Runs the program in debug mode using `-m pdb`.
- `activate`:    Setting up venv to start with
- `deactivate`:  Deleting venv to clean up
- `build`:       Building the whl to dist folder
- `install`:     Builds and installs mazegen-1.0.0-py3-none-any.whl as an example in dist folder
- `clean`:       Deletes artifacts, such as `.mypy_cache` files and `__pycache__` folders.
- `lint`:        Checks for norme compliance.
- `lint-strict`: Checks for norme compliance in strict mode.

Rules can be run by the command `make [rule]`. It is recommended to use venv (`make activate`) for mypy functionality.

# Resources
To gain an understanding of concepts like Depth First Search and Prim's Algorithm, we used websites such as [GeeksforGeeks](https://www.geeksforgeeks.org/).

Generative AI (namely [Gemini](https://gemini.google.com/)) was used to gain a deeper understanding of the python syntax and python functions.

# Details

### Config File
The configuration file holds info on how the maze should generate. This is done using mandatory key-value-pairs: `width`, `height`, `entry`, `exit`, `output_file`, `perfect`, `seed`, and `algorithm`. No other keys are accepted.

The default configuration file (`config.txt`) holds usage information:
```bash
# === Default Configuration === #

# '<int>' Dimensions (>0)
    # Note: No 42 logo when width < 9 and height < 6.
width       = 10
height      = 10

# '<int>,<int>' Tile Coordinates (>-1, <bounds)
    # Note: These are 0-indexed.
entry       = 0, 0
exit        = 9, 9

# '<str>' Solution File Name
    # Note: Contains tile walls in hexadecimal notation (0x[W][S][E][N])
    # Note: Contains entry, exit and solution string (e.g. 'SEESENNW')
output_file = maze.txt

# 'False|No|0 or True|Yes|1' Dead-Ends Possibility
    # Note: Big mazes will have at least 2 dead-ends because of the 42 logo
perfect     = True

# '<int>' Generation Seed
    # Note: Any re-generations will pick a random seed.
seed        = 67

# 'dfs or prims' Generation algorithm
    # Note: 'Depth-First Search' uses one main branch
    # Note: 'Prim's Algorithm' uses
algorithm   = dfs

```
The whole config file (except the value of output_file) is not case-sensitive and may have white-spaces.

### Generation Algorithms
| Algorithm | Description |
| - | - |
| Depth-First Search | Explores a maze by going as deep as possible along each path before backtracking when hitting dead ends. |
| Randomized Prim's | Generates a maze by starting at one cell and continually picking a random wall from its growing border (frontier) to carve into unvisited space, creating a natural, highly branched layout. |

The reason for picking these is that they are the most commonly used algorithms in maze generation. Additionally, DFS and PRIMS offer two different approaches to the same problem (namely river-like and advancing frontier).

### Reusability
maze_generator is a standalone module able to be built to dist/maze_generator-xxx.whl and can be installed via pip install.

```python
# Instantiate
width: int = 5
height: int = 5
entry: list[int] = [0, 0]
exit: list[int] = [4, 4]
seed: int = -101
mg = maze_generator.MazeGenerator(width, height, entry, exit, seed)

# Generate
algorithm: Literal["dfs", "prims"] = "dfs"
mg.generate_maze(algorithm)

# Touch up to make imperfect (no-dead-end)
mg.nde()

# Output
file = "output.txt"
mg.write_maze_to_file(file)
```

### Project Management
Seeing that this is a group project, it was not possible for every group member to do everything.
Basic devision of tasks was for `wchu` to do the back-end (algorithms and output file generation) and for `ldreger` to handle the front-end (config passing and display logic). This devision has persisted throughout the project and is particularly well suited for this project, since that way we clearly knew which part belonged to who, eliminating doubling the work.