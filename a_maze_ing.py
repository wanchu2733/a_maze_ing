import config
import maze_generator
import random
import renderer


def main() -> int:
    c = config.Config.load_config("config.txt")
    random.seed(c._seed)
    mg = maze_generator.MazeGenerator(
        c._width, c._height, c._entry, c._exit, c._seed
    )
    mg.generate_maze(c._algorithm)
    mg.write_maze_to_file(c._output_file)
    return 0


if __name__ == "__main__":
    main()
    renderer.Renderer()
