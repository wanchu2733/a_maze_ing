from maze_generator import algorithm
import maze_generator.algorithm
from typing import Callable


class MazeGenerator:
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    class Cell:
        def __init__(
            self, r: int, c: int, n: bool, e: bool, s: bool, w: bool
        ) -> None:
            self._r = r
            self._c = c
            self._is_42 = False
            self._visited = False
            self._walls = [n, e, s, w]
            self._path: list[str] = []

        def to_hex(self) -> str:
            if self._is_42:
                return "F"
            return f"{sum(self._walls[i] << i for i in range(4)):X}"

    def __init__(
        self, width: int, height: int,
        entry: list[int], exit: list[int], seed: int
    ) -> None:
        self._width = width
        self._height = height
        self._entryr = entry[1]
        self._entryc = entry[0]
        self._exitr = exit[1]
        self._exitc = exit[0]
        self._seed = seed
        self._maze = [
            [
                MazeGenerator.Cell(
                    r,
                    c,
                    c == 0,
                    r == self._width - 1,
                    c == self._height - 1,
                    r == 0,
                ) for c in range(self._width)
            ]
            for r in range(self._height)
        ]
        if self._width < 9 or self._height < 6:
            print("too small, no 42")
        else:
            self._draw_42_at((self._height >> 1) - 2, (self._width >> 1) - 3)

    def find_connection(self, c: Cell) -> Cell:
        lst = [
            ac for dr, dc in MazeGenerator.directions
            if (ac := self.get_cell(c._r + dr, c._c + dc)) and ac._visited
        ]
        i = algorithm.Solver.grfl(lst)
        return lst[i]

    def connect_cell(self, c1: Cell, c2: Cell) -> None:
        if c2._r - 1 == c1._r:
            c1._walls[2] = False
            c2._walls[0] = False
            c2._path = c1._path + ["S"]
        elif c2._r + 1 == c1._r:
            c1._walls[0] = False
            c2._walls[2] = False
            c2._path = c1._path + ["N"]
        elif c2._c - 1 == c1._c:
            c1._walls[1] = False
            c2._walls[3] = False
            c2._path = c1._path + ["E"]
        elif c2._c + 1 == c1._c:
            c1._walls[3] = False
            c2._walls[1] = False
            c2._path = c1._path + ["W"]

    def connect_new_cell(self, c: Cell) -> None:
        ac = self.find_connection(c)
        self.connect_cell(ac, c)

    def atac(self, f: Callable[[Cell], None]) -> None:
        for r in self._maze:
            for c in r:
                f(c)

    def cvc(self, r: int, c: int) -> bool:
        cc = self.get_cell(r, c)
        return not (
            r < 0 or c >= self._width or
            c < 0 or r >= self._height or
            not cc or cc._visited or cc._is_42)

    def gnfc(self, c: Cell | None) -> list[Cell]:
        return [
            cell
            for dr, dc in MazeGenerator.directions
            if c and self.cvc(c._r + dr, c._c + dc)
            and (cell := self.get_cell(c._r + dr, c._c + dc)) is not None
        ]

    def get_cell(self, r: int, c: int) -> Cell | None:
        return (
            None
            if r < 0 or c < 0 or c >= self._width or r >= self._height
            else self._maze[r][c]
        )

    def generate_maze(self, alg: str) -> None:
        solver: maze_generator.algorithm.Solver = self._get_solver(alg)
        solver.solve(self)

    def write_maze_to_file(self, out_fp: str) -> None:
        data = ""
        for r in range(self._height):
            for c in range(self._width):
                data += self._maze[r][c].to_hex()
            data += "\n"
        data += "\n"
        data += f"{self._entryc},{self._entryr}\n"
        data += f"{self._exitc},{self._exitr}\n"
        data += "".join(
            next(
                cc._path for _ in [0] if (
                    cc := self.get_cell(self._exitr, self._exitc)
                ) is not None
            )
        )
        with open(out_fp, "w") as file:
            file.write(data)

    def _draw_42_f(self, r: int, c: int) -> None:
        self._maze[r][c]._is_42 = True

    def _draw_42_at(self, r: int, c: int) -> None:
        self._draw_42_line_at(r, c, 3, False, self._draw_42_f)
        self._draw_42_line_at(r + 2, c, 3, True, self._draw_42_f)
        self._draw_42_line_at(r + 2, c + 2, 3, False, self._draw_42_f)
        self._draw_42_line_at(r, c + 4, 3, True, self._draw_42_f)
        self._draw_42_line_at(r + 2, c + 4, 3, True, self._draw_42_f)
        self._draw_42_line_at(r + 4, c + 4, 3, True, self._draw_42_f)
        self._draw_42_line_at(r, c + 6, 3, False, self._draw_42_f)
        self._draw_42_line_at(r + 2, c + 4, 3, False, self._draw_42_f)

    def _draw_42_line_at(
        self, r: int, c: int, n: int, is_h: bool, f: Callable[[int, int], None]
    ) -> None:
        for i in range(n):
            f(r + (0 if is_h else i), c + (i if is_h else 0))

    def _get_solver(self, alg: str) -> maze_generator.algorithm.Solver:
        if alg.lower() == "dfs":
            return maze_generator.algorithm.DFS()
        elif alg.lower() == "prims":
            return maze_generator.algorithm.Prims()
        raise ValueError("gg")
