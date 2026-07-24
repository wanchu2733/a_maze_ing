from maze_generator import algorithm
import maze_generator.algorithm
from typing import Callable


class MazeGenerator:
    """
    MazeGenerator class, all maze data needed is here
    """
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    class Cell:
        """
        Maze Cell class, the cell grid
        """
        def __init__(
            self, r: int, c: int, n: bool, e: bool, s: bool, w: bool
        ) -> None:
            """__init__ the Cell

            Args:
                r: row index
                c: column index
                n: north wall open close states
                e: east wall open close states
                s: south wall open close states
                w: west wall open close states

            Returns:
                None
            """
            self._r = r
            self._c = c
            self._is_42 = False
            self._visited = False
            self._walls = [n, e, s, w]
            self._path: list[str] = []

        def to_hex(self) -> str:
            """printing the hex value of the cell

            Args:
                self: self

            Returns:
                the single hex code char
            """
            if self._is_42:
                return "F"
            return f"{sum(self._walls[i] << i for i in range(4)):X}"

        def __str__(self) -> str:
            return f"c[{self._r},{self._c}]"

    def __init__(
        self, width: int, height: int,
        entry: list[int], exit: list[int], seed: int
    ) -> None:
        """__init__ the Mazegenerator class

        Args:
            self: self
            width: width of the maze
            height: height of the maze
            entry: entry of the maze
            exit: exit of the maze
            seed: seed of the maze

        Returns:
            None
        """
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
        if self._width >= 9 and self._height >= 6:
            self._draw_42_at((self._height >> 1) - 2, (self._width >> 1) - 3)
    
    def nde(self) -> None:
        """no dead end? ok, no dead end now

        Args:
            self: self

        Returns:
            the visited cell
        """
        for r in self._maze:
            for c in r:
                if not c._is_42 and sum(c._walls) > 2:
                    cn = self.nde_find_connection(c)
                    if cn:
                        self.connect_cell(c, cn)
        algorithm.Solver.fsp(self)
    
    def nde_find_connection(self, c: Cell) -> Cell | None:
        """find a random connection to a visited cell

        Args:
            self: self
            c: the unvisited cell

        Returns:
            the visited cell
        """
        lst = [
            ac for dr, dc in MazeGenerator.directions
            if (ac := self.get_cell(c._r + dr, c._c + dc)) and not ac._is_42 and not self.nde_cvc(c, ac)
        ]
        if len(lst):
            return lst[0]
        else:
            return None

    def find_connection(self, c: Cell) -> Cell:
        """find a random connection to a visited cell

        Args:
            self: self
            c: the unvisited cell

        Returns:
            the visited cell
        """
        lst = [
            ac for dr, dc in MazeGenerator.directions
            if (ac := self.get_cell(c._r + dr, c._c + dc)) and ac._visited and not ac._is_42
        ]
        i = algorithm.Solver.grfl(lst)
        return lst[i]

    def connect_cell(self, c1: Cell, c2: Cell) -> None:
        """connecting the neightbouring cells

        Args:
            self: self
            c1: the from cell
            c2: the to cell

        Returns:
            None
        """
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
        """connecting a unvisited cell to a visited cell

        Args:
            self: self
            c: the new unvisited cell

        Returns:
            None
        """
        ac = self.find_connection(c)
        self.connect_cell(ac, c)

    def atac(self, f: Callable[[Cell], None]) -> None:
        """apply to all cells

        Args:
            self: self
            f: the function to apply to all cells

        Returns:
            None
        """
        for r in self._maze:
            for c in r:
                f(c)

    def cvc(self, r: int, c: int) -> bool:
        """check valid cell

        Args:
            self: self
            r: the cell row index
            c: the cell column index

        Returns:
            is valid boolean
        """
        cc = self.get_cell(r, c)
        return not (
            r < 0 or c >= self._width or
            c < 0 or r >= self._height or
            not cc or cc._visited or cc._is_42)
    
    def fsp_cvc(self, c1: Cell, c2: Cell) -> bool:
        """find shortest path check valid cell

        Args:
            self: self
            c1: cell from
            c2: cell to

        Returns:
            is valid boolean
        """

        if c1 is None or c2 is None or c2._visited:
            return False
        if c2._r - 1 == c1._r and c1._walls[2] == False and c2._walls[0] == False:
            c2._path = c1._path + ["S"]
            return True
        elif c2._r + 1 == c1._r and c1._walls[0] == False and c2._walls[2] == False:
            c2._path = c1._path + ["N"]
            return True
        elif c2._c - 1 == c1._c and c1._walls[1] == False and c2._walls[3] == False:
            c2._path = c1._path + ["E"]
            return True
        elif c2._c + 1 == c1._c and c1._walls[3] == False and c2._walls[1] == False:
            c2._path = c1._path + ["W"]
            return True
        return False

    def nde_cvc(self, c1: Cell, c2: Cell) -> bool:
        """find shortest path check valid cell

        Args:
            self: self
            c1: cell from
            c2: cell to

        Returns:
            is valid boolean
        """

        if c1 is None or c2 is None:
            return False
        if c2._r - 1 == c1._r and c1._walls[2] == False and c2._walls[0] == False:
            return True
        elif c2._r + 1 == c1._r and c1._walls[0] == False and c2._walls[2] == False:
            return True
        elif c2._c - 1 == c1._c and c1._walls[1] == False and c2._walls[3] == False:
            return True
        elif c2._c + 1 == c1._c and c1._walls[3] == False and c2._walls[1] == False:
            return True
        return False
    
    def fsp_gnfc(self, c: Cell | None) -> list[Cell]:
        """find shortest path get next from cell

        Args:
            self: self
            c: the current cell

        Returns:
            list of cells ready to be consumed
        """
        return [
            cell
            for dr, dc in MazeGenerator.directions
            if c and self.fsp_cvc(c, (cell := self.get_cell(c._r + dr, c._c + dc)))
        ]

    def gnfc(self, c: Cell | None) -> list[Cell]:
        """get next from cell

        Args:
            self: self
            c: the current cell

        Returns:
            list of cells ready to be consumed
        """
        return [
            cell
            for dr, dc in MazeGenerator.directions
            if c and self.cvc(c._r + dr, c._c + dc)
            and (cell := self.get_cell(c._r + dr, c._c + dc)) is not None
        ]

    def get_cell(self, r: int, c: int) -> Cell | None:
        """get a cell

        Args:
            self: self
            r: the cell row index
            c: the cell column index

        Returns:
            the cell if exists
        """
        return (
            None
            if r < 0 or c < 0 or c >= self._width or r >= self._height
            else self._maze[r][c]
        )

    def generate_maze(self, alg: str) -> None:
        """choose a solver and solve the maze

        Args:
            self: self
            alg: the algo used to solve, must be valid

        Returns:
            None
        """
        solver: maze_generator.algorithm.Solver = self._get_solver(alg)
        solver.solve(self)

    def write_maze_to_file(self, out_fp: str) -> None:
        """write the maze to hex file

        Args:
            self: self
            out_fp: output file path

        Returns:
            None
        """
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
        """the function to apply to 42 cell

        Args:
            self: self
            r: row index
            c: column index

        Returns:
            None
        """
        self._maze[r][c]._is_42 = True

    def _draw_42_at(self, r: int, c: int) -> None:
        """draw 42 starting at row and column

        Args:
            self: self
            r: row index
            c: column index

        Returns:
            None
        """
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
        """draw 42 lines at row and column

        Args:
            self: self
            r: row index
            c: column index
            n: number of cells in length
            is_h: is horizontal
            f: function to apply to the 42 cell

        Returns:
            None
        """
        for i in range(n):
            f(r + (0 if is_h else i), c + (i if is_h else 0))

    def _get_solver(self, alg: str) -> maze_generator.algorithm.Solver:
        """get solver from alg string

        Args:
            self: self
            alg: the algorithm in string, must be valid

        Returns:
            None
        """
        if alg.lower() == "dfs":
            return maze_generator.algorithm.DFS()
        elif alg.lower() == "prims":
            return maze_generator.algorithm.Prims()
        raise ValueError("gg")
