import math
from .bayesian_agent import BayesianAgentRule1


class MinActionAgent(BayesianAgentRule1):

    def pick_next(self, current=None):
        utility = [[0] * self.env.dim for _ in range(self.env.dim)]
        max_util = float("-inf")
        max_cell = None
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                dest = (i, j)
                if current == dest:
                    continue
                utility[i][j] = self._belief[i][j] / self.manhattan(current, dest)
                if utility[i][j] > max_util:
                    max_util = utility[i][j]
                    max_cell = dest

        distance = self.manhattan(current, max_cell)
        if distance != 1 :
            print(f"Distance: {distance}")
        self.travel_count += distance
        return max_cell

