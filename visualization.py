"""
Matplotlib based visualizer
"""

import numpy as np
from itertools import product
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from environment import Environment


class SearchAndDestroy(object):
    open_color_map = {
        "flat": "darkturquoise",
        "hilly": "royalblue",
        "forest": "blue",
        "cave": "navy"
    }

    color_map = {
        "flat": "white",
        "hilly": "silver",
        "forest": "darkgreen",
        "cave": "black"
    }
    covered_color = '#DDDDDD'
    uncovered_color = '#AAAAAA'
    edge_color = '#888888'
    count_colors = ['none', 'blue', 'green', 'red', 'darkblue',
                    'darkred', 'darkgreen', 'black', 'black']
    flag_vertices = np.array([[0.25, 0.2], [0.25, 0.8],
                              [0.75, 0.65], [0.25, 0.5]])

    def __init__(self, env: Environment):
        self.env = env
        self.width = self.env.dim
        self.height = self.env.dim
        self.target = self.env.target
        self.open_count = np.zeros((self.env.dim, self.env.dim))

        # define internal state variables
        self.flags = np.zeros((self.width, self.height), dtype=object)


        # generate figure
        plt.figure(figsize=((self.width + 2) / 3., (self.height + 2) / 3.))
        self.fig, self.ax = plt.subplots(1, 2)

        self.generate_fig(self.ax[0])
        self.generate_fig(self.ax[1])

        # self.ax2 = self.generate_fig(ax[1])
        self.game_over = False

    def generate_fig(self, ax):
        ax_loc = (0.05, 0.05, 0.9, 0.9)
        width, height, target = self.env.dim, self.env.dim, self.env.target
        # Create the figure and axes
        ax.set_xlim(-ax_loc[0], width + ax_loc[0])
        ax.set_ylim(-ax_loc[1], height + ax_loc[1])
        ax.set_aspect('equal')

        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_formatter(plt.NullFormatter())
            axis.set_major_locator(plt.NullLocator())

        # Create the grid of squares
        squares = np.array([[RegularPolygon((i + 0.5, j + 0.5),
                                                 numVertices=4,
                                                 radius=0.5 * np.sqrt(2),
                                                 orientation=np.pi / 4,
                                                 ec=self.edge_color,
                                                 fc=self.color_map[self.env.get_terrain(i, j).name])
                                  for i in range(height)]
                                 for j in range(width)])

        [ax.add_patch(sq) for sq in squares.flat]
        # map(self.ax.add_path, self.squares.flat)

        # draw the target
        self._draw_target(ax, *target)

    def _draw_target(self, ax, i, j):
        ax.add_patch(plt.Circle((i + 0.5, j + 0.5), radius=0.25,
                                     ec='black', fc='red'))

    def update(self, i, j, belief):
        # checking bounds
        if i < 0 or j < 0 or i >= self.width or j >= self.height:
            return
        belief = round(belief, 3)
        self.open_count[i, j] += 1
        self.ax[1].add_patch(RegularPolygon((i + 0.5, j + 0.5),
                                            numVertices=4,
                                            radius=0.5 * np.sqrt(2),
                                            orientation=np.pi / 4,
                                            ec=self.edge_color,
                                            fc=self.open_color_map[self.env.get_terrain(i, j).name])
                             )
        if (i, j) == self.env.target:
            self._draw_target(self.ax[1], i, j)

        if self.open_count[i, j] > 1:
            self.ax[1].text(i + 0.5, j + 0.5, int(self.open_count[i, j]),
                            color="yellow", ha='center', va='center', fontsize=10,
                            fontweight='bold')

        self.fig.canvas.draw()
        plt.pause(0.2)
        # input()

    def show(self):
        plt.ion()
        self.fig.show()
