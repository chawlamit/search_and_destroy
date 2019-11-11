from agents.bayesian_agent_rule1 import BayesianAgentRule1


class BayesianAgentRule2(BayesianAgentRule1):

    def pick_next(self, current=None):
        max_prob = float("-inf")
        cell = None
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                terrain = self.env.get_terrain(i, j)
                prob_finding_target = self._belief[i][j] * (1 - terrain.p_false_neg)
                if prob_finding_target > max_prob:
                    max_prob = prob_finding_target
                    cell = (i, j)

        distance = self.manhattan(current, cell)
        self.travel_count += distance
        return cell
