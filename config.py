from typing import Optional
from maze_generator import MazeGenerator


class Config:
    def __init__(self) -> None:
        self._width: int | None = None
        self._height: int | None = None
        self._entry: list[int] | None = None
        self._exit: list[int] | None = None
        self._output_file: str | None = None
        self._perfect: bool | None = None
        self._seed: int | None = None
        self._algorithm: str = "dfs"

    def is_pass_fail(self) -> str:
        if self._width is None or self._height is None:
            return ("Missing width or height:\n"
                    "Width and height must have a value.")
        if self._entry is None or self._exit is None:
            return ("Missing entry or exit:\n"
                    "Entry and exit must have ','-delimited coords.")
        if self._output_file is None:
            return ("Missing output file name:\n"
                    "Output file must have a valid name.")
        if self._perfect is None:
            return ("Missing Perfect Boolean:\n"
                    "Perfect must have a valid boolean value "
                    "(e.g. 'false', 'yes', '0', ...).")
        if self._seed is None:
            return ("Missing seed value:\n"
                    "Seed must be a valid integer.")
        if self._algorithm is None:
            return ("Missing algorithm:\n"
                    "Algorithm must be recognized ('dfs', 'prims').")
        return ""

    def is_invalid(self, maze_gen: MazeGenerator) -> str:
        assert self._width is not None
        assert self._height is not None
        if self._width <= 0 or self._height <= 0:
            return ("Maze Bounds Too Low:\n"
                    "Width and height must be greater than 0.")

        assert self._entry is not None
        assert self._exit is not None
        if self._entry == self._exit:
            return ("Same Coordinates:\n"
                    "Entry and exit coords must be different.")
        if (self._entry[0] > self._width - 1
                or self._exit[0] > self._width - 1):
            return ("Exceeding Maze Width:\n"
                    "Entry and exit x-coords must not be greater than width.")
        if (self._entry[0] < 0 or self._exit[0] < 0):
            return ("Exceeding Maze Width:\n"
                    "Entry and exit x-coords must not be negative.")
        if (self._entry[1] > self._height - 1
                or self._exit[1] > self._height - 1):
            return ("Exceeding Maze Height:\n"
                    "Entry and exit y-coords must not be greater than height.")
        if (self._entry[1] < 0 or self._exit[1] < 0):
            return ("Exceeding Maze Height:\n"
                    "Entry and exit y-coords must not be negative.")
        if maze_gen._maze[self._entry[1]][self._entry[0]]._is_42:
            return ("Invalid Entry Coordinates:\n"
                    "Entry coords may not fall on 42 logo.")
        if maze_gen._maze[self._exit[1]][self._exit[0]]._is_42:
            return ("Invalid Exit Coordinates:\n"
                    "Exit coords may not fall on 42 logo.")

        assert self._output_file is not None
        if not self._output_file:
            return ("Missing output file:\n"
                    "Output file name must be a valid file name.")

        assert self._perfect is not None
        if not isinstance(self._perfect, bool):
            return ("Invalid Perfect Boolean:\n"
                    "Perfect must have a valid boolean value "
                    "(e.g. 'false', 'yes', '0', ...).")

        return ""

    @staticmethod
    def load_config_1(ln: str, config: "Config") -> None:
        """Load config helper

        Args:
            ln: config line, must be valid
            config: the config content to write to

        Returns:
            None
        """
        if ln.count("=") != 1:
            return
        k, v = ln.split("=")
        an = f"_{k.strip().lower()}"
        rv = v.strip()
        if not rv:
            return

        if hasattr(config, an):
            if an in ("_width", "_height", "_seed"):
                try:
                    setattr(config, an, int(rv))
                except ValueError:
                    return
            elif an in ("_perfect",):
                if rv.lower() in ("true", "yes", "1"):
                    setattr(config, an, True)
                elif rv.lower() in ("false", "no", "0"):
                    setattr(config, an, False)
                else:
                    setattr(config, an, rv)
            elif an in ("_entry", "_exit"):
                try:
                    setattr(config, an, [int(n) for n in rv.split(",")])
                except ValueError:
                    return
            else:
                setattr(config, an, rv)

    @staticmethod
    def load_config(path: str) -> Optional["Config"]:
        """Load config from path

        Args:
            path: the path to config file, default config.txt

        Returns:
            Config
        """
        config = Config()
        try:
            with open(path) as file:
                data = file.readlines()
                for ln in data:
                    if not ln or ln.startswith("#"):
                        continue
                    Config.load_config_1(ln, config)
        except FileNotFoundError:
            return None
        return config
