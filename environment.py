from terrain import Terrain
import random
import numpy as np


class Environment:
    def __init__(self, dim=50, p_flat=0.2, p_hilly=0.3 , p_forest=0.3, p_cave=0.2, place_target_in="random"):
        self.dim = dim
        self.p_flat = p_flat
        self.p_hilly = p_hilly
        self.p_forest = p_forest
        self.p_cave = p_cave
        self._create_board()
        # Place the target
        self.target = None
        self.place_target(place_target_in)

    def _create_board(self):
        self._board = np.array([ [None]*self.dim for _ in range(self.dim) ])

        multinomial_sample = np.random.multinomial(self.dim ** 2, [1/4] * 4, size=1)
        for i in range(self.dim):
            for j in range(self.dim) :
                sample = np.random.randint(0, 4)
                while multinomial_sample[0, sample] == 0:
                    sample = np.random.randint(0, 4)
                multinomial_sample[0,sample] -= 1
                self._board[i, j] = Terrain.generate_from_index(sample)

    def generate_from_sample(self, sample_env):
        self.dim = len(sample_env)
        for i, row in enumerate(sample_env):
            for j, terrain in enumerate(row):
                f = getattr(Terrain, 'generate_' + terrain)
                self._board[i][j] = f()

    def place_target(self, terrain):
        target = np.random.randint(0, (self.dim ** 2) - 1)
        row, col = target // self.dim, target % self.dim

        if terrain == "random" or terrain not in Terrain.T_names:
            pass
        else:
            while self.get_terrain(row, col).name != terrain:
                target = np.random.randint(0, self.dim ** 2 + 1)
                row, col = target // self.dim, target % self.dim

        self.target = (row, col)

    def search(self, row, col):
        if (row, col) != self.target:
            return False
        p = self._board[row, col].p_false_neg
        if np.random.binomial(1, 1-p, 1):
            return True
        else:
            return False

    # Helper Funcs
    def get_terrain(self, row, col):
        return self._board[row, col]

    def show(self):
        for row in self._board :
            print(row)
        print()

    def get_neighbors(self, row, col):
        """
        :return: List of neighbours out of the 4 valid neighbours
        """
        nbs = []
        if 0 <= row - 1 < self.dim and 0 <= col < self.dim:
            nbs.append((row-1, col))
        if 0 <= row + 1 < self.dim and 0 <= col < self.dim:
            nbs.append((row+1, col))
        if 0 <= row < self.dim and 0 <= col - 1 < self.dim:
            nbs.append((row, col-1))
        if 0 <= row < self.dim and 0 <= col + 1 < self.dim:
            nbs.append((row, col+1))
        return nbs




