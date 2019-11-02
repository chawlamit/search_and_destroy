from environment import Environment
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self,env:Environment):
        self.env = env
        self.search_count = 0
        self._belief = [[(1 / self.env.dim ** 2, (i, j)) for j in range(env.dim)] for i in range(env.dim)]

    @abstractmethod
    def run(self):
        pass

    def search(self):
        self.search_count += 1
        return self.env.search()
