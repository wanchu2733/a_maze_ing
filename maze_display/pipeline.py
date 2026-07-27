from __future__ import annotations
from typing import TYPE_CHECKING
import time
from maze_display.structures import Pos, MenuState, Color

if TYPE_CHECKING:
    from maze_display.renderer import Renderer


class Pipeline():
    def __init__(self, context: Renderer, block_width: int):
        self.ctx: Renderer = context
        self._block_width: int = block_width

        self._border_block_str: str = f"{self.ctx.color['border']}██\x1b[0m"
        self._wall_block_str: str = f"{self.ctx.color['wall']}██\x1b[0m"
        self._start_block_str: str = f"{self.ctx.color['start']}██\x1b[0m"
        self._exit_block_str: str = f"{self.ctx.color['exit']}██\x1b[0m"
        self._maze_str: str = ""

        self.is_anim: bool = True
        self.anim_speed: float = 0.01
        self.crnt_step: int = 0

    def reserve_space(self) -> None:
        """Fills _maze_str with correct amount of lines and spaces.

        One block is prefilled with "██\\x1b[0m",
        each line is delimited by "\\n".
        """
        self._border_block_str = f"{self.ctx.color['border']}██\x1b[0m"
        self._wall_block_str = f"{self.ctx.color['wall']}██\x1b[0m"
        self._start_block_str = f"{self.ctx.color['start']}██\x1b[0m"
        self._exit_block_str = f"{self.ctx.color['exit']}██\x1b[0m"
        self._maze_str = ""
        for ln in range(self.ctx.maze_height * 2 + 1):
            if ln == 0 or ln == self.ctx.maze_height * 2:
                for ltr in range(self.ctx.maze_width * 2 - 1):
                    self._maze_str += self._border_block_str
            else:
                for ltr in range(self.ctx.maze_width * 2 - 1):
                    if ltr == 0 or ltr == self.ctx.maze_width * 2 - 2:
                        self._maze_str += self._border_block_str
                    else:
                        self._maze_str += self._wall_block_str
            self._maze_str += "\n"

    def add_logo_color(self) -> None:
        for y in range(self.ctx.maze_height):
            if self.ctx.data[y] == "\n":
                break
            for x in range(self.ctx.maze_width):
                if (self.ctx.data[y][x] == "F"):
                    self.set_block(Pos(x * 2 + 1, y * 2 + 1), "logo")

    def get_block(self, tile_pos: Pos) -> int:
        """Gets the index position of _maze_str matching tile_pos.

        Args:
            tile_pos (Pos): Position of tile to get the index from.

        Returns:
            int: Index of tile.
        """
        row: int = 0
        display_list: list[str] = self._maze_str.split("\n")
        for i in range(tile_pos.y):
            row += len(display_list[i]) + 1

        col: int = 0
        row_list: list[str] = display_list[tile_pos.y].split("\x1b[0m")
        for i in range(tile_pos.x):
            col += len(row_list[i]) + len("\x1b[0m")

        return row + col

    def set_block(self, tile_pos: Pos, keyword: str) -> None:
        """Sets tile position to a certain color.

        Args:
            tile_pos (Pos): Position of tile to re-color.
            keyword (str): Color to set tile to.
        """
        idx: int = self.get_block(tile_pos)

        display_list: list[str] = self._maze_str.split("\n")
        row_list: list[str] = display_list[tile_pos.y].split("\x1b[0m")
        prev_block_len = len(row_list[tile_pos.x])

        color_id: str = ""
        if keyword in self.ctx.color.keys():
            color_id = self.ctx.color[keyword]

        pre: str = self._maze_str[:idx]
        post: str = self._maze_str[idx + prev_block_len:]
        self._maze_str = pre + color_id + "██" + post

    def display(self, is_wait: bool = True) -> int:
        """Clears screen, draws maze, feedback message, and menu.

        Args:
            is_wait (bool, optional): Whether to display waiting menu.
                Defaults to True.
        """
        print("\x1bc\x1b[3J", end="")
        print(self._maze_str)
        print(self.ctx.inputter.feedback_msg)
        if self.ctx.inputter.is_quitting:
            return 1

        if is_wait:
            self.ctx.inputter.wait_menu(self.crnt_step // 20 % 4)
            return 0

        match self.ctx.inputter.menu_state:
            case MenuState.main:
                self.ctx.inputter.main_menu()
            case MenuState.tile:
                self.ctx.inputter.tile_menu()
            case MenuState.color:
                self.ctx.inputter.color_menu()
            case MenuState.respeed:
                self.ctx.inputter.respeed_menu()
        return 0

    def step(self, tile_pos: Pos, keyword: str, is_wait: bool = True) -> int:
        """Recolors a tile, displays, and possibly waits.

        Args:
            tile_pos (Pos): Position of tile to re-color.
            keyword (str): Color to set tile to.
            is_wait (bool, optional): her to display waiting menu.
                Defaults to True.
        """
        self.crnt_step += 1
        self.set_block(tile_pos, keyword)
        if self.display(is_wait):
            return 1
        if self.is_anim and self.anim_speed > 0:
            try:
                time.sleep(self.anim_speed)
            except (KeyboardInterrupt, EOFError):
                self.ctx.inputter.feedback_msg = (
                    f"{Color.ERR}Keyboard interrupt, "
                    f"aborting.{Color.END}"
                )
                self.ctx.inputter.is_quitting = True
        return 0

    def is_path(self, tile_pos: Pos) -> bool:
        """Checks if tile falls on shortest path.

        Args:
            tile_pos (Pos): Position of tile to check.

        Returns:
            bool: True if tile is a path.
        """
        return (tile_pos.x in self.ctx.pathdict
                and tile_pos.y in self.ctx.pathdict[tile_pos.x])


class BlockyPipeline(Pipeline):
    def __init__(self, context: "Renderer"):
        super().__init__(context, 2)

    def gen_render(self) -> None:
        if self.ctx.ani is None:
            return
        for update in self.ctx.ani:
            if self.update_tile(Pos(update[1], update[0]), update[2]):
                return

    def update_tile(self, tile_pos: Pos, hex: str) -> int:
        hexadecimal: str = "0123456789ABCDEF"
        block_pos: Pos = Pos(tile_pos.x * 2 + 1, tile_pos.y * 2 + 1)

        if self.ctx.startpos == tile_pos:
            self.set_block(block_pos, "start")
        elif self.ctx.exitpos == tile_pos:
            self.set_block(block_pos, "exit")
        else:
            self.set_block(block_pos, "background")

        if not (hexadecimal.index(hex) & 0b0001):
            self.set_block(Pos(block_pos.x, block_pos.y - 1), "background")
        if not (hexadecimal.index(hex) & 0b0010):
            self.set_block(Pos(block_pos.x + 1, block_pos.y), "background")
        if not (hexadecimal.index(hex) & 0b0100):
            self.set_block(Pos(block_pos.x, block_pos.y + 1), "background")
        if not (hexadecimal.index(hex) & 0b1000):
            self.set_block(Pos(block_pos.x - 1, block_pos.y), "background")

        self.crnt_step += 1
        if self.display():
            return 1
        if self.is_anim and self.anim_speed > 0:
            try:
                time.sleep(self.anim_speed)
            except (KeyboardInterrupt, EOFError):
                self.ctx.inputter.feedback_msg = (
                    f"{Color.ERR}Keyboard interrupt, "
                    f"aborting.{Color.END}"
                )
                self.ctx.inputter.is_quitting = True
        return 0

    def maze_render(self) -> None:
        """Draws maze line by line, tile by tile."""
        for y in range(self.ctx.maze_height):
            if self.ctx.data[y] == "\n":
                break
            for x in range(self.ctx.maze_width):
                if self.upper_tiling(Pos(x, y)):
                    return
            if self.step(
                Pos((self.ctx.maze_width - 1) * 2, y * 2),
                "border"
            ):
                return
            for x in range(self.ctx.maze_width):
                if self.lower_tiling(Pos(x, y)):
                    return
            if self.step(
                Pos((self.ctx.maze_width - 1) * 2, y * 2 + 1),
                "border"
            ):
                return
        i: int = 0
        while i < self.ctx.maze_width * 2 - 1:
            if self.step(Pos(i, self.ctx.maze_height * 2), "border"):
                return
            i += 1

    def upper_tiling(self, tile_pos: Pos) -> int:
        """Draws the upper blocks of tiles.

        Args:
            tile_pos (Pos): Position of tile.
        """
        hexadecimal: str = "0123456789ABCDEF"
        block_pos: Pos = Pos(tile_pos.x * 2, tile_pos.y * 2)

        if self.ctx.data[tile_pos.y][tile_pos.x] == "\n":
            return 0
        if hexadecimal.index(self.ctx.data[tile_pos.y][tile_pos.x]) & 0b0001:
            if tile_pos.x == 0 or tile_pos.y == 0:
                if self.step(block_pos, "border"):
                    return 1
            else:
                if self.step(block_pos, "wall"):
                    return 1
            block_pos.x += 1
            if tile_pos.y == 0:
                if self.step(block_pos, "border"):
                    return 1
            else:
                if self.step(block_pos, "wall"):
                    return 1
        else:
            if tile_pos.x == 0:
                if self.step(block_pos, "border"):
                    return 1
            else:
                if self.step(block_pos, "wall"):
                    return 1
            block_pos.x += 1
            if (
                self.ctx.is_show_path
                and self.ctx.is_path_drawing
                and self.is_path(tile_pos)
                and self.is_path(Pos(tile_pos.x, tile_pos.y - 1))
            ):
                if self.step(block_pos, "path"):
                    return 1
            else:
                if self.step(block_pos, "background"):
                    return 1
        return 0

    def lower_tiling(self, tile_pos: Pos) -> int:
        """Draws the lower blocks of tiles.

        Args:
            tile_pos (Pos): Position of tile.
        """
        hexadecimal: str = "0123456789ABCDEF"
        block_pos: Pos = Pos(tile_pos.x * 2, tile_pos.y * 2 + 1)

        if self.ctx.data[tile_pos.y][tile_pos.x] == "\n":
            return 0
        if hexadecimal.index(self.ctx.data[tile_pos.y][tile_pos.x]) & 0b1000:
            if tile_pos.x == 0:
                if self.step(block_pos, "border"):
                    return 1
            else:
                if self.step(block_pos, "wall"):
                    return 1
        else:
            if (
                self.ctx.is_show_path
                and self.ctx.is_path_drawing
                and tile_pos.x > 0
                and self.is_path(tile_pos)
                and self.is_path(Pos(tile_pos.x - 1, tile_pos.y))
            ):
                if self.step(block_pos, "path"):
                    return 1
            else:
                if self.step(block_pos, "background"):
                    return 1
        block_pos.x += 1
        if self.ctx.data[tile_pos.y][tile_pos.x] == "F":
            if self.step(block_pos, "logo"):
                return 1
        elif (
            tile_pos.x == self.ctx.startpos.x
            and tile_pos.y == self.ctx.startpos.y
        ):
            if self.step(block_pos, "start"):
                return 1
        elif (
            tile_pos.x == self.ctx.exitpos.x
            and tile_pos.y == self.ctx.exitpos.y
        ):
            if self.step(block_pos, "exit"):
                return 1
        elif (
            self.ctx.is_show_path
            and self.ctx.is_path_drawing
            and self.is_path(tile_pos)
        ):
            if self.step(block_pos, "path"):
                return 1
        else:
            if self.step(block_pos, "background"):
                return 1
        return 0

    def draw_path(self) -> None:
        """Draws path in steps specified in in maze.txt."""
        self.ctx.is_path_drawing = True
        for pos in self.ctx.pathlist:
            self.upper_tiling(pos)
            self.lower_tiling(pos)
