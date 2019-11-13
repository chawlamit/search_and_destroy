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

    def __init__(self, env: Environment, belief, delay=0.2):
        self.env = env
        self.belief = belief
        self.delay = delay
        self.width = self.env.dim
        self.height = self.env.dim
        self.target = self.env.target
        self.open_count = np.zeros((self.env.dim, self.env.dim))
        self.ann_ref = [[None] * self.env.dim for _ in range(self.env.dim)]
        # define internal state variables
        self.flags = np.zeros((self.width, self.height), dtype=object)

        # generate figure
        plt.figure(figsize=((self.width + 2) / 3., (self.height + 2) / 3.))
        self.fig, self.ax = plt.subplots(1, 2)

        self.generate_fig(self.ax[0])
        self.generate_fig(self.ax[1])

        # show belief on annotation
        self.annot_belief = self.ax[1].annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot_belief.set_visible(False)

        self.fig.canvas.mpl_connect('motion_notify_event', self.show_belief)

    def generate_fig(self, ax):
        ax_loc = (0.05, 0.05, 0.9, 0.9)
        width, height, target = self.env.dim, self.env.dim, self.env.target
        # Create the figure and axes
        ax.set_xlim(-ax_loc[0], width + ax_loc[0])
        ax.set_ylim(-ax_loc[1], height + ax_loc[1])
        ax.set_aspect('equal')
        ax.invert_yaxis()

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
                                for j in range(width)]
                            for i in range(height)])

        [ax.add_patch(sq) for sq in squares.flat]
        # map(self.ax.add_path, self.squares.flat)

        # draw the target
        self._draw_target(ax, *target)

    def _draw_target(self, ax, i, j):
        # clear prev_target for movingTarget
        if hasattr(self.env, 'prev_target') and self.env.prev_target is not None:
            if self.open_count[self.env.prev_target[0], self.env.prev_target[1]] > 0:
                color = self.open_color_map[self.env.get_terrain(*self.env.prev_target).name]
            else:
                color = self.color_map[self.env.get_terrain(*self.env.prev_target).name]
            ax.add_patch(RegularPolygon((self.env.prev_target[0] + 0.5, self.env.prev_target[1] + 0.5),
                                        numVertices=4,
                                        radius=0.5 * np.sqrt(2),
                                        orientation=np.pi / 4,
                                        ec=self.edge_color,
                                        fc=color))
        # draw target
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
        # if (i, j) == self.env.target:
        self._draw_target(self.ax[1], *self.env.target)

        if self.open_count[i, j] > 1:
            if self.ann_ref[i][j] is None:
                self.ann_ref[i][j] = self.ax[1].annotate(int(self.open_count[i, j]), (i + 0.5, j + 0.5),
                                                         color="yellow", ha='center', va='center', fontsize=10,
                                                         fontweight='bold')
            else:
                self.ann_ref[i][j].set_text(int(self.open_count[i, j]))
        self.fig.canvas.draw()
        plt.pause(self.delay)
        # input()

    def show_belief(self, event):
        try:
            x = int(event.xdata)
            y = int(event.ydata)
            if event.inaxes == self.ax[1]:
                self.annot_belief.set_text(round(self.belief[x, y], 4))
                self.annot_belief.xy = (x + 0.5, y + 0.5)
                self.annot_belief.set_visible(True)
        except Exception as e:
            self.annot_belief.set_visible(False)

    def show(self):
        plt.ion()
        self.fig.show()
