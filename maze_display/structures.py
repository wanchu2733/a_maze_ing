from enum import Enum
from dataclasses import dataclass


class MenuState(Enum):
    """Represents menu stages of inputter.

    Attributes:
        main: The main menu screen.
        title: The title menu screen when re-setting color.
        color: The color screen only showing after the title screen.
        respeed: The animation speed adjust screen.
    """
    main = 1
    tile = 2
    color = 3
    respeed = 4


@dataclass
class Pos:
    """Two-dimentional position in maze."""
    x: int
    y: int


@dataclass
class Color:
    """ASCII Color codes."""
    black: str = "\x1b[30m"
    red: str = "\x1b[31m"
    green: str = "\x1b[32m"
    yellow: str = "\x1b[33m"
    blue: str = "\x1b[34m"
    magenta: str = "\x1b[35m"
    cyan: str = "\x1b[36m"
    white: str = "\x1b[37m"
    bright_black: str = "\x1b[90m"
    bright_red: str = "\x1b[91m"
    bright_green: str = "\x1b[92m"
    bright_yellow: str = "\x1b[93m"
    bright_blue: str = "\x1b[94m"
    bright_magenta: str = "\x1b[95m"
    bright_cyan: str = "\x1b[96m"
    bright_white: str = "\x1b[97m"

    EMPTY: str = ""
    ERR: str = "\x1b[31m"
    WRN: str = "\x1b[33m"
    SCS: str = "\x1b[32m"
    LES: str = "\x1b[90m"
    SRT: str = "\x1b[35m"
    EXT: str = "\x1b[34m"
    END: str = "\x1b[0m"
