from typing import Optional
from maze_generator import MazeGenerator
from maze_display.structures import Color


class Config:
    def __init__(self) -> None:
        self._width: int | None = None
        self._height: int | None = None
        self._entry: list[int] | None = None
        self._exit: list[int] | None = None
        self._output_file: str | None = None
        self._perfect: bool | None = None
        self._seed: int | None = None
        self._algorithm: str | None = None

    def is_pass_fail(self) -> str:
        """Checks if any attributes were not set in config file

        Returns:
            str: "" on success, len(str) > 0 for error
        """
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

    def is_invalid(self) -> str:
        """Checks if provided values make sense

        Args:
            maze_gen (MazeGenerator): Maze class to check if entry/exit
                falls into logo

        Returns:
            str: "" on success, len(str) > 0 for error
        """
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

        assert self._output_file is not None
        if not self._output_file:
            return ("Missing output file:\n"
                    "Output file name must be a valid file name.")

        assert self._perfect is not None
        if not isinstance(self._perfect, bool):
            return ("Invalid Perfect Boolean:\n"
                    "Perfect must have a valid boolean value "
                    "(e.g. 'false', 'yes', '0', ...).")

        assert self._algorithm is not None
        if not (self._algorithm.lower() == "dfs"
                or self._algorithm.lower() == "prims"):
            return ("Invalid Generation Algorithm:\n"
                    "Algorithm must be recognized ('dfs', 'prims').")

        return ""

    def is_coords_invalid(self, maze_gen: MazeGenerator) -> str:
        """Checks if entry and exit fall on logo

        Args:
            maze_gen (MazeGenerator): Maze class to check if entry/exit
                falls into logo

        Returns:
            str: "" on success, len(str) > 0 for error
        """
        assert self._entry is not None and self._exit is not None
        if maze_gen._maze[self._entry[1]][self._entry[0]]._is_42:
            return ("Invalid Entry Coordinates:\n"
                    "Entry coords may not fall on 42 logo.")
        if maze_gen._maze[self._exit[1]][self._exit[0]]._is_42:
            return ("Invalid Exit Coordinates:\n"
                    "Exit coords may not fall on 42 logo.")

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
        if ln.strip() == "":
            return
        if ln.count("=") != 1:
            raise KeyError(f"\"{ln}\" does not "
                           "follow KEY=Value format.")
        k, v = ln.split("=")
        an = f"_{k.strip().lower()}"
        rv = v.strip()
        if not rv:
            raise KeyError(f"\"{k.strip()}\" does not "
                           "follow KEY=Value format.")

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
            elif an in ("_output_file", "_algorithm"):
                setattr(config, an, rv)
        else:
            raise KeyError(f"Key \"{k.strip()}\" not recognized.")

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
                    if not ln or ln.strip().startswith("#"):
                        continue
                    try:
                        Config.load_config_1(ln, config)
                    except KeyError as e:
                        print(f"{Color.ERR}Error when passing config file: "
                              f"{e}{Color.END}")
                        return None
        except (FileNotFoundError, PermissionError, IsADirectoryError):
            print(f"{Color.ERR}'{path}' file not found.{Color.END}")
            return None
        return config
