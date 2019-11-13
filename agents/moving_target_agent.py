"""
Bonus Improvement Step: Augment the agent, when the tracker is moving
"""
from agents.bayesian_agent_rule1 import BayesianAgentRule1
from agents.min_action_agent import MinActionAgent
from environment import Environment
from terrain import Terrain
import numpy as np
import random


class MovingTargetEnvironment(Environment):
    # Bonus part - For Moving target

    def __init__(self, dim=50, p_flat=0.2, p_hilly=0.3, p_forest=0.3, p_cave=0.2, place_target_in="random"):
        super().__init__(dim, p_flat, p_hilly, p_forest, p_cave, place_target_in)
        self.prev_target = None

    def gps(self):
        """
        Faulty gps on target, returns a terrain type where the target is not located
        :return: <string> - name of Terrain where target is not located
        """
        terrain = self.get_terrain(*self.target)
        # Pick random terrain where the target is not located
        target_not_in = random.choice(Terrain.T_names)
        while target_not_in == terrain.name:
            target_not_in = random.choice(Terrain.T_names)

        return target_not_in

    def move_target(self):
        """
        Moves target to one of the 4 neighbors uniformly
        :return:
        """
        self.prev_target = self.target
        self.target = random.choice(self.get_neighbors(*self.target))

    def search(self, row, col):
        search_result = super().search(row, col)
        if not search_result:
            self.move_target()
        return search_result


class MovingTargetAgent_Rule1(BayesianAgentRule1):
    
    def pick_next(self, current=None):
        """
        Picks a cell with max belief of containing the target ignoring the terrain where target is not present
        :param current:
        :return:
        """
        # get gps reading
        target_not_in = self.env.gps()
        print(f'target not in: {target_not_in}')

        belief_cells = {}
        max_belief_ex_t = -1
        for i, row in enumerate(self._belief):
            for j, prob in enumerate(row):
                if self.env.get_terrain(i, j).name == target_not_in:
                    continue
                if self._belief[i, j] == max_belief_ex_t:
                    belief_cells[max_belief_ex_t].append((i, j))
                if self._belief[i, j] > max_belief_ex_t:
                    # purge old max belief to save some space
                    if max_belief_ex_t in belief_cells:
                        belief_cells.pop(max_belief_ex_t)
                    # update new max belief
                    max_belief_ex_t = self._belief[i, j]
                    if max_belief_ex_t not in belief_cells:
                        belief_cells[max_belief_ex_t] = []
                    belief_cells[max_belief_ex_t].append((i, j))

        dest = random.choice(belief_cells[max_belief_ex_t])
        distance = self.manhattan(current, dest)
        self.travel_count += distance
        return dest


class MovingTargetAgent_MinAction(BayesianAgentRule1):

    def pick_next(self, current=None):
        target_not_in = self.env.gps()
        print(f'target not in: {target_not_in}')

        utility = [[0] * self.env.dim for _ in range(self.env.dim)]

        util_cells = {}
        max_util = -1
        max_cell = None
        for i, row in enumerate(self._belief):
            for j, prob in enumerate(row):
                if self.env.get_terrain(i, j).name == target_not_in or current == (i, j):
                    continue
                utility[i][j] = prob / self.manhattan(current, (i, j))
                if utility[i][j] == max_util:
                    util_cells[max_util].append((i, j))
                if utility[i][j] > max_util:
                    if max_util in util_cells:
                        util_cells.pop(max_util)
                    # add this new max
                    max_util = utility[i][j]
                    if max_util not in util_cells:
                        util_cells[max_util] = []
                    util_cells[max_util].append((i, j))

        max_cell = random.choice(util_cells[max_util])
        distance = self.manhattan(current, max_cell)
        if distance != 1:
            print(f"Distance: {distance}")
        self.travel_count += distance
        return max_cell
