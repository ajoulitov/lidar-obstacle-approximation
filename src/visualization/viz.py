import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Circle as MplCircle
from typing import List, Tuple
from geom_core import Segment, Circle


class Visualizer:
    def __init__(
            self,
            ax=None,
            max_range: float = 5.0,
            title: str = "Webots Lidar View",
            figsize: Tuple[float, float] = (6, 6)
    ):
        self.max_range = max_range
        self.title = title

        if ax is None:
            plt.ion()
            self.fig, self.ax = plt.subplots(figsize=figsize)
        else:
            self.fig = ax.figure
            self.ax = ax

        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_title(self.title)

        self.scat = self.ax.scatter([], [], s=3, c='k', label='Obstacles')

        self.robot_point, = self.ax.plot([0], [0], 'ro', markersize=8, markeredgecolor='black', label='Robot')
        arrow_len = float(self.max_range) * 0.2 if self.max_range is not None else 3.0
        self.arrow = FancyArrow(0, 0, 0, arrow_len, width=arrow_len * 0.12, length_includes_head=True, alpha=0.6)
        self.ax.add_patch(self.arrow)

        self._segment_lines = []
        self._circle_patches = []

        self.ax.legend(loc='upper right')

        self._set_limits_default()

        plt.show(block=False)
        plt.pause(0.001)

    def _set_limits_default(self):
        if self.max_range is not None:
            limit = float(self.max_range) * 1.1
        else:
            limit = 1.0
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)

    def update_points(self, pts: np.ndarray):
        if pts is None or pts.size == 0:
            self.scat.set_offsets(np.empty((0, 2)))
        else:
            self.scat.set_offsets(pts)

        if self.max_range is None and pts is not None and pts.size > 0:
            limit = max(np.max(np.abs(pts[:, 0])), np.max(np.abs(pts[:, 1])))
            limit = max(limit * 1.1, 1.0)
            self.ax.set_xlim(-limit, limit)
            self.ax.set_ylim(-limit, limit)

        self._redraw()

    def update_primitives(self, segments: List[Segment], circles: List[Circle]):
        for ln in self._segment_lines:
            try:
                ln.remove()
            except Exception:
                pass
        for cp in self._circle_patches:
            try:
                cp.remove()
            except Exception:
                pass
        self._segment_lines.clear()
        self._circle_patches.clear()

        for seg in segments:
            ln, = self.ax.plot([seg.p1.x, seg.p2.x], [seg.p1.y, seg.p2.y], '-', linewidth=1.5, color='b',
                               label='_nolegend_')
            self._segment_lines.append(ln)

        for c in circles:
            circ = MplCircle((c.center.x, c.center.y), c.radius, fill=False, linewidth=1.5, linestyle='-',
                             label='_nolegend_')
            self.ax.add_patch(circ)
            self._circle_patches.append(circ)

        self._redraw()

    def _redraw(self):
        handles, labels = self.ax.get_legend_handles_labels()
        unique = {}
        for h, l in zip(handles, labels):
            if l not in unique and not l.startswith('_nolegend_'):
                unique[l] = h
        if unique:
            self.ax.legend(unique.values(), unique.keys(), loc='upper right')
        plt.draw()
        plt.pause(0.001)
