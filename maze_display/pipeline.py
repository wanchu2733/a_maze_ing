from __future__ import annotations
from typing import TYPE_CHECKING
import time
from maze_display.structures import Pos, MenuState

if TYPE_CHECKING:
    from maze_display.renderer import Renderer


class Pipeline():
    def __init__(self, context: "Renderer", block_width: int):
        self.ctx: Renderer = context
        self._block_width: int = block_width

        self._default_block_str: str = self.ctx.color["background"]
        for space in range(self._block_width):
            self._default_block_str += "█"
        self._default_block_str += "\033[0m"
        self._maze_str: str = ""

        self.is_anim: bool = True
        self.anim_speed: float = 0.01
        self.crnt_step: int = 0

    def reserve_space(self) -> None:
        """Fills _maze_str with correct amount of lines and spaces.

        One block is prefilled with "██\\033[0m",
        each line is delimited by "\\n".
        """
        self._maze_str = ""
        for ln in range(self.ctx.maze_height * 2 + 1):
            for ltr in range(self.ctx.maze_width * 2 - 1):
                self._maze_str += self._default_block_str
            self._maze_str += "\n"

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
        row_list: list[str] = display_list[tile_pos.y].split("\033[0m")
        for i in range(tile_pos.x):
            col += len(row_list[i]) + len("\033[0m")

        return row + col

    def set_block(self, tile_pos: Pos, keyword: str) -> None:
        """Sets tile position to a certain color.

        Args:
            tile_pos (Pos): Position of tile to re-color.
            keyword (str): Color to set tile to.
        """
        idx: int = self.get_block(tile_pos)

        display_list: list[str] = self._maze_str.split("\n")
        row_list: list[str] = display_list[tile_pos.y].split("\033[0m")
        prev_block_len = len(row_list[tile_pos.x])

        color_id: str = ""
        if keyword in self.ctx.color.keys():
            color_id = self.ctx.color[keyword]

        pre: str = self._maze_str[:idx]
        post: str = self._maze_str[idx + prev_block_len:]
        self._maze_str = pre + color_id + "██" + post

    def display(self, is_dummy: bool = True) -> None:
        """Clears screen, draws maze, feedback message, and menu.

        Args:
            is_dummy (bool, optional): Whether to display dummy (waiting) menu.
                Defaults to True.
        """
        print("\033c", end="")
        print(self._maze_str)
        print(self.ctx.inputter.feedback_msg)
        if self.ctx.inputter.is_quitting:
            return
        if is_dummy:
            self.ctx.inputter.dummy_menu(self.crnt_step // 20 % 4)
            return

        match self.ctx.inputter.menu_state:
            case MenuState.main:
                self.ctx.inputter.main_menu()
            case MenuState.tile:
                self.ctx.inputter.tile_menu()
            case MenuState.color:
                self.ctx.inputter.color_menu()

    def step(self, tile_pos: Pos, keyword: str, is_dummy: bool = True) -> None:
        """Recolors a tile, displays, and possibly waits.

        Args:
            tile_pos (Pos): Position of tile to re-color.
            keyword (str): Color to set tile to.
            is_dummy (bool, optional): her to display dummy (waiting) menu.
                Defaults to True.
        """
        self.crnt_step += 1
        self.set_block(tile_pos, keyword)
        self.display(is_dummy)
        if self.is_anim:
            time.sleep(self.anim_speed)

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

    def maze_render(self) -> None:
        """Draws maze line by line, tile by tile."""
        for y in range(self.ctx.maze_height):
            if self.ctx.data[y] == "\n":
                break
            for x in range(self.ctx.maze_width):
                self.upper_tiling(Pos(x, y))
            self.step(
                Pos((self.ctx.maze_width - 1) * 2, y * 2),
                "border"
            )
            for x in range(self.ctx.maze_width):
                self.lower_tiling(Pos(x, y))
            self.step(
                Pos((self.ctx.maze_width - 1) * 2, y * 2 + 1),
                "border"
            )
        i: int = 0
        while i < self.ctx.maze_width * 2 - 1:
            self.step(Pos(i, self.ctx.maze_height * 2), "border")
            i += 1

    def upper_tiling(self, tile_pos: Pos) -> None:
        """Draws the upper blocks of tiles.

        Args:
            tile_pos (Pos): Position of tile.
        """
        hexadecimal: str = "0123456789ABCDEF"
        block_pos: Pos = Pos(tile_pos.x * 2, tile_pos.y * 2)

        if self.ctx.data[tile_pos.y][tile_pos.x] == "\n":
            return
        if hexadecimal.index(self.ctx.data[tile_pos.y][tile_pos.x]) & 0b0001:
            if tile_pos.x == 0 or tile_pos.y == 0:
                self.step(block_pos, "border")
            else:
                self.step(block_pos, "wall")
            block_pos.x += 1
            if tile_pos.y == 0:
                self.step(block_pos, "border")
            else:
                self.step(block_pos, "wall")
        else:
            if tile_pos.x == 0:
                self.step(block_pos, "border")
            else:
                self.step(block_pos, "wall")
            block_pos.x += 1
            if (
                self.ctx.is_show_path
                and self.ctx.is_path_drawing
                and self.is_path(tile_pos)
                and self.is_path(Pos(tile_pos.x, tile_pos.y - 1))
            ):
                self.step(block_pos, "path")
            else:
                self.step(block_pos, "background")

    def lower_tiling(self, tile_pos: Pos) -> None:
        """Draws the lower blocks of tiles.

        Args:
            tile_pos (Pos): Position of tile.
        """
        hexadecimal: str = "0123456789ABCDEF"
        block_pos: Pos = Pos(tile_pos.x * 2, tile_pos.y * 2 + 1)

        if self.ctx.data[tile_pos.y][tile_pos.x] == "\n":
            return
        if hexadecimal.index(self.ctx.data[tile_pos.y][tile_pos.x]) & 0b1000:
            if tile_pos.x == 0:
                self.step(block_pos, "border")
            else:
                self.step(block_pos, "wall")
        else:
            if (
                self.ctx.is_show_path
                and self.ctx.is_path_drawing
                and tile_pos.x > 0
                and self.is_path(tile_pos)
                and self.is_path(Pos(tile_pos.x - 1, tile_pos.y))
            ):
                self.step(block_pos, "path")
            else:
                self.step(block_pos, "background")
        block_pos.x += 1
        if self.ctx.data[tile_pos.y][tile_pos.x] == "F":
            self.step(block_pos, "logo")
        elif (
            tile_pos.x == self.ctx.startpos.x
            and tile_pos.y == self.ctx.startpos.y
        ):
            self.step(block_pos, "start")
        elif (
            tile_pos.x == self.ctx.endpos.x
            and tile_pos.y == self.ctx.endpos.y
        ):
            self.step(block_pos, "exit")
        elif (
            self.ctx.is_show_path
            and self.ctx.is_path_drawing
            and self.is_path(tile_pos)
        ):
            self.step(block_pos, "path")
        else:
            self.step(block_pos, "background")

    def draw_path(self) -> None:
        """Draws path in steps specified in in maze.txt."""
        self.ctx.is_path_drawing = True
        for pos in self.ctx.pathlist:
            self.upper_tiling(pos)
            self.lower_tiling(pos)
