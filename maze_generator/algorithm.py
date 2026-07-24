import maze_generator
import random


class Solver:
    """
    Base class for DFS and Prims, could be ABC.
    """
    def solve(self, mg: "maze_generator.MazeGenerator") -> None:
        """Generic solve function, abstract layer

        Args:
            self: self
            mg: the maze generator class

        Returns:
            None
        """
        print("solver from solver")

    @staticmethod
    def grfl(cl: list["maze_generator.MazeGenerator.Cell"]) -> int:
        """Get random from list, returning index

        Args:
            cl: the list of Cells to choose from

        Returns:
            the index of the choosen one
        """
        return random.randint(0, len(cl) - 1)

    @staticmethod
    def _init_wall(c: "maze_generator.MazeGenerator.Cell") -> None:
        """Initialise walls in maze generator to all closed not visited

        Args:
            c: the maze generator cell

        Returns:
            None
        """
        c._walls = [True] * len(c._walls)
        c._visited = False
    
    @staticmethod
    def _fsp_init_wall(c: "maze_generator.MazeGenerator.Cell") -> None:
        """Initialise find shortest path walls in maze generator to all closed not visited

        Args:
            c: the maze generator cell

        Returns:
            None
        """
        c._visited = False
        c._path = []

    @staticmethod
    def fsp(mg: "maze_generator.MazeGenerator") -> None:
        """Find shortest path and store in cell._path

        Args:
            mg: maze_generator.MazeGenerator

        Returns:
            None
        """
        mg.atac(Solver._fsp_init_wall)
        cc = mg.get_cell(mg._entryr, mg._entryc)
        if not cc:
            return
        ft = [cc]
        nft = []
        cc._visited = True
        while len(ft):
            while len(ft):
                sc = ft.pop(0)
                sc._visited = True
                nfc = mg.fsp_gnfc(sc)
                nft.extend(nfc)
            ft.extend(set(nft) - set(ft))
            nft = []
        

class DFS(Solver):
    def solve(self, mg: "maze_generator.MazeGenerator") -> None:
        """Generic solve function override, solving the maze in cell

        Args:
            self: self
            mg: the maze generator class

        Returns:
            None
        """
        self._mg = mg
        self._mg.atac(Solver._init_wall)
        cstk = (
            [r for _ in [0] if (
                r := self._mg.get_cell(self._mg._entryr, self._mg._entryc)
            ) is not None]
        )
        cstk[0]._visited = True
        while len(cstk) > 0:
            nb = self._mg.gnfc(cstk[-1])
            if len(nb) == 0:
                cstk.pop()
                continue
            i = self.grfl(nb)
            sc = nb[i]
            sc._visited = True
            self._mg.connect_cell(cstk[-1], sc)
            cstk.append(sc)


class Prims(Solver):
    def solve(self, mg: "maze_generator.MazeGenerator") -> None:
        """Generic solve function override, solving the maze in cell

        Args:
            self: self
            mg: the maze generator class

        Returns:
            None
        """
        self._mg = mg
        self._mg.atac(Solver._init_wall)
        cc = self._mg.get_cell(self._mg._entryr, self._mg._entryc)
        if not cc:
            return
        ft = self._mg.gnfc(cc)
        cc._visited = True
        while len(ft) > 0:
            i = self.grfl(ft)
            sc = ft.pop(i)
            sc._visited = True
            self._mg.connect_new_cell(sc)
            nft = self._mg.gnfc(sc)
            ft.extend(set(nft) - set(ft))
