from .base_agent import BaseAgent
import random

class BayesianAgentRule1(BaseAgent):
    """
    Using bayesian update to update the belief of Ta = Ci for every cell on board given the data we observed i.e. T != Ci
    Ta -> actual location of Target, T -> result returned about the state of target

    Baysian Update: P(Ta = Ci / data) => P(Ta = Ci and data) / P(data)
    """

    #TODO - normalize probability after each update cycle
    def P_data(self, prior, p_false_neg):
        # P(T != Cj) = { P(Ta = Cj) X P(T != Cj)   +  P(Ta != Cj) X P(T != Cj)
        #                 Prior     X P_false_neg  +  (1 - Prior) X 1
        return prior * p_false_neg + (1 - prior) * 1

    def update(self, current_cell, searched_cell, prior, p_false_neg):

        if current_cell == searched_cell:
            posterior = prior * p_false_neg / self.P_data(prior, p_false_neg)
        else:
            prior_current_cell = self._belief[current_cell[0]][current_cell[1]]
            posterior = prior_current_cell / self.P_data(prior, p_false_neg)
        self._belief[current_cell[0]][current_cell[1]] = posterior

    def pick_next(self, current=None):
        max_belief_cells = []
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                if self._belief[i][j] == self.max_belief:
                    max_belief_cells.append((i, j))

        dest = random.choice(max_belief_cells)
        distance = self.manhattan(current, dest)
        self.travel_count += distance
        return dest


    def run(self):
        prev_cell = (0, 0)
        while True:
            # self.show()
            current = self.pick_next(prev_cell)
            terrain = self.env.get_terrain(*current)
            # print(f"current: {current}, terrain: {terrain}")

            found = self.search(*current)
            if found:
                break

            self.max_belief = -1
            prior = self._belief[current[0]][current[1]]
            for i, row in enumerate(self._belief):
                for j, prob in enumerate(row):
                    self.update((i, j), current, prior, terrain.p_false_neg)
                    if self._belief[i][j] > self.max_belief:
                        self.max_belief = self._belief[i][j]
            prev_cell = current


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


