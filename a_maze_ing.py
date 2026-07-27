import config
import maze_generator
import maze_display.renderer
from maze_display.structures import Color
import sys


def generate_output(
        seed: int | None = None
        ) -> tuple[config.Config | None, list[tuple[int, int, str]] | None]:
    """Opens config file, passes value, results in output file

    Returns:
        config.Config: Config class with config file data
    """
    if len(sys.argv) != 2:
        print(f"{Color.ERR}No config file found. ",
              f"Provide it as an argument{Color.END}")
        return (None, None)
    c = config.Config.load_config(sys.argv[1])
    if not c:
        return (None, None)
    if c.is_pass_fail():
        print(f"{Color.ERR}{c.is_pass_fail()}{Color.END}")
        return (None, None)

    if seed is not None:
        c._seed = seed
    assert c._width is not None and c._height is not None
    assert c._entry is not None and c._exit is not None
    assert c._seed is not None
    mg = maze_generator.MazeGenerator(
        c._width, c._height, c._entry, c._exit, c._seed
    )
    if c.is_invalid(mg):
        print(f"{Color.ERR}{c.is_invalid(mg)}{Color.END}")
        return (None, None)

    assert c._algorithm is not None
    mg.generate_maze(c._algorithm)
    if not c._perfect:
        mg.nde()
    assert c._output_file is not None
    mg.write_maze_to_file(c._output_file)

    return (c, mg._ani)


def main() -> int:
    """Generates maze and solution, displays it.

    Returns:
        int: 0 for successful exit, 1 for error.
    """
    c, ani = generate_output()
    if not c or not ani:
        return 1

    try:
        assert c._output_file is not None and ani is not None
        r = maze_display.renderer.Renderer(c._output_file, ani)
        assert c._width is not None and c._height is not None
        if c._width < 9 or c._height < 6:
            r.inputter.feedback_msg = (f"{Color.LES}Maze is too small: "
                                       f"Skipping 42 logo.{Color.END} ")
        r.inputter.feedback_msg += (f"{Color.LES}(SEED: {c._seed}){Color.END}")
        r.main_render()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        print(f"{Color.ERR}Data not found, aborting.{Color.END}")

    return 0


if __name__ == "__main__":
    main()
