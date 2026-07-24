from maze_display.structures import Color, Pos
import maze_display.pipeline as pipeline
import maze_display.inputter as inputter


class Renderer():
    def __init__(self, file_name: str):
        self.color: dict[str, str] = {
            "background": Color.black,
            "border": Color.bright_white,
            "wall": Color.white,
            "start": Color.magenta,
            "exit": Color.blue,
            "path": Color.yellow,
            "logo": Color.bright_black
        }
        self.data: list[str] = []
        self.maze_width: int = 0
        self.maze_height: int = 0
        self.startpos: Pos = Pos(0, 0)
        self.endpos: Pos = Pos(0, 0)
        self.pathdict: dict[int, list[int]] = {}
        self.pathlist: list[Pos] = []
        self.is_show_path: bool = True
        self.is_path_drawing: bool = False

        try:
            with open(file_name) as file:
                self.data = file.readlines()
                for ln in range(len(self.data)):
                    if self.data[ln] == "\n":
                        break
                    self.maze_height += 1
                self.maze_width = len(self.data[0])
                self.startpos.x = int(
                    self.data[len(self.data) - 3].split(",")[0]
                )
                self.startpos.y = int(
                    self.data[len(self.data) - 3].split(",")[1]
                )
                self.endpos.x = int(
                    self.data[len(self.data) - 2].split(",")[0]
                )
                self.endpos.y = int(
                    self.data[len(self.data) - 2].split(",")[1]
                )
                self.fill_pathdata(self.data[len(self.data) - 1])
        except FileNotFoundError:
            print(f"{Color.ERR}Data not found, aborting.{Color.END}")
            return

        self.pipeline: pipeline.BlockyPipeline = pipeline.BlockyPipeline(self)
        self.inputter: inputter.Inputter = inputter.Inputter(self)

    def main_render(self) -> None:
        """Renders maze, draws path, and returns control to user"""
        self.pipeline.reserve_space()
        self.pipeline.maze_render()
        if self.is_show_path:
            self.pipeline.draw_path()
        self.pipeline.display(False)

    def fill_pathdata(self, directions: str) -> None:
        """Fills pathdict and pathlist attributes

        Args:
            directions (str): Sequence of maze.txt of shortest path
        """
        crnt_x: int = self.startpos.x
        crnt_y: int = self.startpos.y

        if crnt_x not in self.pathdict:
            self.pathdict[crnt_x] = []
        self.pathdict[crnt_x].append(crnt_y)
        self.pathlist.append(Pos(crnt_x, crnt_y))
        for dir_idx in range(len(directions)):
            match directions[dir_idx]:
                case "N":
                    crnt_y -= 1
                case "S":
                    crnt_y += 1
                case "E":
                    crnt_x += 1
                case "W":
                    crnt_x -= 1
            if crnt_x not in self.pathdict:
                self.pathdict[crnt_x] = []
            self.pathdict[crnt_x].append(crnt_y)
            self.pathlist.append(Pos(crnt_x, crnt_y))
