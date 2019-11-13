import math
import random
from .bayesian_agent_rule1 import BayesianAgentRule1


class MinActionAgent(BayesianAgentRule1):

    def pick_next(self, current=None):
        utility = [[0] * self.env.dim for _ in range(self.env.dim)]

        util_cells = {}
        max_util = -1
        max_cell = None
        for i, row in enumerate(self._belief):
            for j, prob in enumerate(row):
                if current == (i, j):
                    continue
                utility[i][j] = prob / self.manhattan(current, (i, j))

                if utility[i][j] > max_util:
                    if max_util in util_cells:
                        util_cells.pop(max_util)
                    # add this new max
                    max_util = utility[i][j]
                    if max_util not in util_cells:
                        util_cells[max_util] = []
                    util_cells[max_util].append((i, j))

                if utility[i][j] == max_util:
                    util_cells[max_util].append((i, j))

        max_cell = random.choice(util_cells[max_util])
        distance = self.manhattan(current, max_cell)
        if distance != 1:
            print(f"Distance: {distance}")
        self.travel_count += distance
        return max_cell
