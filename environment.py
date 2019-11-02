from terrain import Terrain
import numpy as np
from pprint import pprint

class Environment() :
    def __init__(self, dim=50, p_flat=0.2, p_hilly=0.3 , p_forest=0.3, p_cave=0.2 ):
        self.dim = dim
        self.p_flat = p_flat
        self.p_hilly = p_hilly
        self.p_forest = p_forest
        self.p_cave = p_cave
        self._create_board()
        self.target = self._place_target()

    def _create_board(self):
        self._board = np.array([ [None]*self.dim for _ in range(self.dim) ])

        multinomial_sample = np.random.multinomial(self.dim ** 2, [1/4] * 4, size = 1)
        for i in range(self.dim) :
            for j in range(self.dim) :
                sample = np.random.randint(0, 4 )
                while multinomial_sample[0,sample] == 0 :
                    sample = np.random.randint(0, 4 )
                multinomial_sample[0,sample] -= 1
                self._board[i,j] = Terrain.generate_from_index(sample)

    def _place_target(self):
        target = np.random.randint(0, self.dim ** 2 + 1)
        row, col = target // self.dim, target % self.dim
        return row, col

    def search(self, row, col):
        if (row, col) != self.target:
            return False
        p = self._board[row,col].p_false_neg
        if np.random.binomial(1,1-p,1):
            return True
        else:
            return False

    def show(self):
        for row in self._board :
            print(row)
        print()





