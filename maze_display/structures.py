from enum import Enum
from dataclasses import dataclass


class MenuState(Enum):
    """Represents menu stages of inputter.

    Attributes:
        main: The main menu screen.
        title: The title menu screen when re-setting color.
        color: The color screen only showing after the title screen.
    """
    main = 1
    tile = 2
    color = 3


@dataclass
class Pos:
    """Two-dimentional position in maze."""
    x: int
    y: int


@dataclass
class Color:
    """ASCII Color codes."""
    black: str = "\033[30m"
    red: str = "\033[31m"
    green: str = "\033[32m"
    yellow: str = "\033[33m"
    blue: str = "\033[34m"
    magenta: str = "\033[35m"
    cyan: str = "\033[36m"
    white: str = "\033[37m"
    bright_black: str = "\033[90m"
    bright_red: str = "\033[91m"
    bright_green: str = "\033[92m"
    bright_yellow: str = "\033[93m"
    bright_blue: str = "\033[94m"
    bright_magenta: str = "\033[95m"
    bright_cyan: str = "\033[96m"
    bright_white: str = "\033[97m"

    EMPTY: str = ""
    ERR: str = "\033[31m"
    WRN: str = "\033[33m"
    SCS: str = "\033[32m"
    LES: str = "\033[90m"
    SRT: str = "\033[35m"
    EXT: str = "\033[34m"
    END: str = "\033[0m"
