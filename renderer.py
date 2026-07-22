import a_maze_ing
from dataclasses import dataclass
from enum import Enum
import time


# def zeige_ladebalken(gesamtschritte: int):
#     breite = 20  # Gesamtlänge des Balkens in Zeichen
    
#     for i in range(gesamtschritte + 1):
#         # 1. Prozentwert berechnen
#         prozent = int((i / gesamtschritte) * 100)
        
#         # 2. Anzahl der gefüllten und leeren Felder berechnen
#         gefuellt = int((i / gesamtschritte) * breite)
#         leer = breite - gefuellt
        
#         # 3. Den Balken als String zusammensetzen
#         balken = "█" * gefuellt + "." * leer
        
#         # 4. Ausgabe mit \r am Anfang und \033[K am Ende
#         # flush=True sorgt dafür, dass das Terminal sofort aktualisiert wird
#         print(f"\rLade: [{balken}] {prozent}%", end="", flush=True)
        
#         # Künstliche Verzögerung für die Animation
#         time.sleep(0.1)
    
#     # Am Ende der Animation eine neue Zeile anfangen
#     print()


class Tile(Enum):
    NONE = 1


@dataclass
class Color:
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


@dataclass
class Pos:
    x: int
    y: int


class Blocky():
    def __init__(self, context: "Renderer"):
        self.ctx: Renderer = context
        self.block_str: str = "!!\033[0m"
        self.crnt_display: str = ""

        for ln in range(self.ctx.maze_height + 1):
            for ltr in range(self.ctx.maze_width * 2 - 1):
                self.crnt_display += self.block_str
            self.crnt_display += "\n"

        self.maze_render()

    def get_block_index(self, tile_pos: Pos) -> int:
        row: int = 0
        display_list: list[str] = self.crnt_display.split("\n")
        for i in range(tile_pos.y):
            row += len(display_list[i]) + 1

        col: int = 0
        row_list: list[str] = display_list[tile_pos.y].split("\033[0m")
        for i in range(tile_pos.x):
            col += len(row_list[i]) + 4

        return row + col

    def change_block(self, tile_pos: Pos, keyword: str):
        idx: int = self.get_block_index(tile_pos)

        display_list: list[str] = self.crnt_display.split("\n")
        row_list: list[str] = display_list[tile_pos.y].split("\033[0m")
        current_block_length = len(row_list[tile_pos.x]) + 4

        color_id: str = ""
        if keyword in self.ctx.color.keys():
            color_id = self.ctx.color[keyword]

        pre: str = self.crnt_display[:idx]
        post: str = self.crnt_display[idx + current_block_length:]
        self.crnt_display = pre + color_id + "██\033[0m" + post

    def display(self) -> None:
        print(self.crnt_display)

    def step(self, tile_pos: Pos, keyword: str) -> None:
        self.change_block(tile_pos, keyword)
        print("\033c")
        self.display()
        time.sleep(0.01)

    def maze_render(self) -> None:
        # for y in range(self.ctx.maze_height):
        #     if self.ctx.data[y] == "\n":
        #         break
        #     for x in range(self.ctx.maze_width):
        #         self.upper_tiling(Pos(x, y))
        #     self.write_block(
        #         Pos((self.ctx.maze_width - 1) * self.block_width, y),
        #         "border"
        #     )
            # for x in range(self.ctx.maze_width):
            #     self.middle_tiling(Pos(x, y))
            # self.write_block(Pos(x, y), "border")
        i: int = 0
        while i < self.ctx.maze_width * 2 - 1:
            self.step(Pos(i, self.ctx.maze_height), "border")
            i += 1

    def upper_tiling(self, x: int, y: int) -> None:
        hexadecimal: str = "0123456789ABCDEF"

        if self.ctx.data[y][x] == "\n":
            return
        if hexadecimal.index(self.ctx.data[y][x]) & 0b0001:
            if x == 0 or y == 0:
                print(f"{self.ctx.color['border']}██{Color.END}", end="")
            else:
                print(f"{self.ctx.color['wall']}██{Color.END}", end="")
            if y == 0:
                print(f"{self.ctx.color['border']}██{Color.END}", end="")
            else:
                print(f"{self.ctx.color['wall']}██{Color.END}", end="")
        else:
            if x == 0:
                print(f"{self.ctx.color['border']}██{Color.END}", end="")
            else:
                print(f"{self.ctx.color['wall']}██{Color.END}", end="")
            if (
                self.ctx.is_show_path
                and y > 0 and x in self.ctx.pathlist
                and y in self.ctx.pathlist[x] and x in self.ctx.pathlist
                and y - 1 in self.ctx.pathlist[x]
            ):
                print(f"{self.ctx.color['path']}██{Color.END}", end="")
            else:
                print("  ", end="")

    def middle_tiling(self, x: int, y: int) -> None:
        hexadecimal: str = "0123456789ABCDEF"

        if self.ctx.data[y][x] == "\n":
            return
        if hexadecimal.index(self.ctx.data[y][x]) & 0b1000:
            if x == 0:
                print(f"{self.ctx.color['border']}██{Color.END}", end="")
            else:
                print(f"{self.ctx.color['wall']}██{Color.END}", end="")
        else:
            if (
                self.ctx.is_show_path
                and x > 0 and x in self.ctx.pathlist
                and y in self.ctx.pathlist[x] and x - 1 in self.ctx.pathlist
                and y in self.ctx.pathlist[x]
            ):
                print(f"{self.ctx.color['path']}██{Color.END}", end="")
            else:
                print("  ", end="")
        if self.ctx.data[y][x] == "F":
            print(f"{self.ctx.color['logo']}██{Color.END}", end="")
        elif x == self.ctx.startpos.x and y == self.ctx.startpos.y:
            print(f"{self.ctx.color['start']}██{Color.END}", end="")
        elif x == self.ctx.endpos.x and y == self.ctx.endpos.y:
            print(f"{self.ctx.color['exit']}██{Color.END}", end="")
        elif (
            self.ctx.is_show_path
            and x in self.ctx.pathlist and y in self.ctx.pathlist[x]
        ):
            print(f"{self.ctx.color['path']}██{Color.END}", end="")
        else:
            print("  ", end="")


class Renderer():
    def __init__(self):
        self.color: dict[str, str] = {
            "border": Color.bright_green,
            "wall": Color.bright_yellow,
            "start": Color.magenta,
            "exit": Color.blue,
            "path": Color.yellow,
            "logo": Color.bright_cyan
        }
        self.data: list[str] = []
        self.maze_width: int = 0
        self.maze_height: int = 0
        self.startpos: Pos = Pos(0, 0)
        self.endpos: Pos = Pos(0, 0)
        self.pathlist: dict[int, list[int]] = {}
        self.is_show_path: bool = True

        # zeige_ladebalken(50)

        try:
            with open("maze.txt") as file:
                self.data = file.readlines()
                self.maze_height = len(self.data)
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
                self.fill_pathlist(self.data[len(self.data) - 1])
        except FileNotFoundError as e:
            print(e)

        self.engine: Blocky = Blocky(self)
        self.main_render()

    def main_render(self) -> None:
        if not self.data:
            print("Data not found, aborting.")
            return
        # self.engine.maze_render()
        self.main_inputter()

    def main_inputter(self) -> None:
        print("\n=== A-Maze-ing ===")
        print(f"{Color.LES}1. Re-generate a new maze{Color.END}")
        print(f"{Color.LES}2. Show / Hide the shortest path{Color.END}")
        print(f"{Color.LES}3. Customize maze{Color.END}")
        print(f"{Color.LES}4. Quit{Color.END}")
        # zeige_ladebalken(50)
        while 1:
            choice = input(f"{Color.SRT}Choice? (1-4): {Color.END}")
            match choice:
                case "1":
                    print(
                        f"{Color.SCS}Generating new maze",
                        f"from config.txt...{Color.END}"
                    )
                    a_maze_ing.main()
                    self.main_render()
                    break
                case "2":
                    if self.is_show_path:
                        print(
                            f"{Color.SCS}Toggling to hide",
                            f"shortest path...{Color.END}"
                        )
                    else:
                        print(
                            f"{Color.SCS}Toggling to show",
                            f"shortest path...{Color.END}"
                        )
                    self.is_show_path = not self.is_show_path
                    self.main_render()
                    break
                case "3":
                    print("A")
                case "4":
                    print(f"{Color.SCS}Quitting process...{Color.END}")
                    break
                case _:
                    print(
                        f"{Color.ERR}Unrecognized input. Try again.{Color.END}"
                    )

    def fill_pathlist(self, directions: str) -> None:
        crnt_x: int = self.startpos.x
        crnt_y: int = self.startpos.y

        if crnt_x not in self.pathlist:
            self.pathlist[crnt_x] = []
        self.pathlist[crnt_x].append(crnt_y)
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
            if crnt_x not in self.pathlist:
                self.pathlist[crnt_x] = []
            self.pathlist[crnt_x].append(crnt_y)
