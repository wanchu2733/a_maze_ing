from maze_display.structures import Color, Pos
import maze_display.pipeline as pipeline
import maze_display.inputter as inputter


class Renderer():
    def __init__(self, output_name: str, ani: list[tuple[int, int, str]]):
        self.color: dict[str, str] = {
            "background": Color.black,
            "border": Color.bright_white,
            "wall": Color.white,
            "start": Color.magenta,
            "exit": Color.blue,
            "path": Color.yellow,
            "logo": Color.bright_black
        }

        self.output_name: str = output_name
        self.ani: list[tuple[int, int, str]] | None = ani
        self.data: list[str] = []
        self.maze_width: int = 0
        self.maze_height: int = 0
        self.startpos: Pos = Pos(0, 0)
        self.exitpos: Pos = Pos(0, 0)
        self.pathdict: dict[int, list[int]] = {}
        self.pathlist: list[Pos] = []
        self.is_show_path: bool = True
        self.is_path_drawing: bool = False

        self.read_output()

        self.pipeline: pipeline.BlockyPipeline = pipeline.BlockyPipeline(self)
        self.inputter: inputter.Inputter = inputter.Inputter(self)

    def read_output(self) -> None:
        """Reads data from the output file and saves it as attributes

        Note that this does not have file not found handling.
        """
        with open(self.output_name) as file:
            self.data = file.readlines()
            self.maze_height = 0
            for ln in range(len(self.data)):
                if self.data[ln] == "\n":
                    break
                self.maze_height += 1
            self.maze_width = len(self.data[0])
            self.startpos.x = int(self.data[len(self.data) - 3].split(",")[0])
            self.startpos.y = int(self.data[len(self.data) - 3].split(",")[1])
            self.exitpos.x = int(self.data[len(self.data) - 2].split(",")[0])
            self.exitpos.y = int(self.data[len(self.data) - 2].split(",")[1])
            self.fill_pathdata(self.data[len(self.data) - 1])

    def main_render(self) -> None:
        """Renders maze, draws path, and returns control to user"""
        self.pipeline.crnt_step = 0
        self.pipeline.reserve_space()
        self.pipeline.add_logo_color()
        self.pipeline.gen_render()
        if self.inputter.is_quitting:
            return
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

        self.pathdict = {}
        self.pathlist = []
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
