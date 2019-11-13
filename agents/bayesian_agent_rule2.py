from agents.bayesian_agent_rule1 import BayesianAgentRule1
import random


class BayesianAgentRule2(BayesianAgentRule1):

    def pick_next(self, current=None):
        cells = {}
        max_prob = -1
        cell = None
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                terrain = self.env.get_terrain(i, j)
                prob_finding_target = self._belief[i][j] * (1 - terrain.p_false_neg)
                if prob_finding_target > max_prob:
                    if max_prob in cells:
                        cells.pop(max_prob)
                    max_prob = prob_finding_target
                    cells[max_prob] = []
                    cells[max_prob].append((i, j))
                if prob_finding_target == max_prob:
                    cells[max_prob].append((i, j))

        cell = random.choice(cells[max_prob])
        distance = self.manhattan(current, cell)
        self.travel_count += distance
        return cell
