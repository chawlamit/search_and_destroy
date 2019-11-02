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

    def show(self):
        for row in self._board :
            print(row)
        print()





