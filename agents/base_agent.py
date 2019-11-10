from environment import Environment
from terrain import Terrain
from visualization import SearchAndDestroy
import numpy as np

from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt

class BaseAgent(ABC):
    def __init__(self, env: Environment, visualize=False):
        self.env = env
        self.search_count = 0
        self.travel_count = 0

        initial_belief = 1 / self.env.dim ** 2
        self._belief = np.array([[initial_belief for j in range(env.dim)] for i in range(env.dim)])
        self.max_belief = initial_belief

        # visualization
        self.visualize = visualize
        if visualize:
            self.visualization = SearchAndDestroy(env)
            self.visualization.show()

    @abstractmethod
    def run(self):
        pass

    def search(self, row, col):
        self.search_count += 1
        return self.env.search(row, col)

    def show(self):
        for row in self._belief:
            print(row)

    def update_visualization(self, row, col):
        if self.visualize:
            self.visualization.update(row, col, self._belief[row][col])

    @staticmethod
    def manhattan(current, dest):
        return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

    def total_actions(self):
        return self.search_count + self.travel_count

