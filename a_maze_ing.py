import config
import maze_generator
import random
import maze_display.renderer
from maze_display.structures import Color
import sys


def main(is_new_render: bool = True) -> int:
    """Opens config file, passes values, generates maze, displays.

    Args:
        is_new_render (bool, optional): Whether to create a new
            Renderer class or not. Defaults to True.

    Returns:
        int: 0 for successful exit, 1 for error.
    """
    if len(sys.argv) != 2:
        print(f"{Color.ERR}No config file found. ",
              f"Provide it as an argument{Color.END}")
        return 1
    c = config.Config.load_config(sys.argv[1])
    if not c:
        print(f"{Color.ERR}'{sys.argv[1]}' file not found.{Color.END}")
        return 1
    if c.is_pass_fail():
        print(f"{Color.ERR}{c.is_pass_fail()}{Color.END}")
        return 1

    random.seed(c._seed)
    assert c._width is not None
    assert c._height is not None
    assert c._entry is not None
    assert c._exit is not None
    assert c._seed is not None
    mg = maze_generator.MazeGenerator(
        c._width, c._height, c._entry, c._exit, c._seed
    )
    if c.is_invalid(mg):
        print(f"{Color.ERR}{c.is_invalid(mg)}{Color.END}")
        return 1
    assert c._algorithm is not None
    mg.generate_maze(c._algorithm)
    assert c._output_file is not None
    if not c._perfect:
        mg.nde()
    mg.write_maze_to_file(c._output_file)

    if is_new_render:
        r = maze_display.renderer.Renderer(c._output_file)
        if c._width < 9 or c._height < 6:
            r.inputter.feedback_msg = (f"{Color.LES}Maze is too small: "
                                       f"Skipping 42 logo.{Color.END}")
        r.main_render()
    return 0


if __name__ == "__main__":
    main()
