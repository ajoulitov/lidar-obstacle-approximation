from ..geom_core import Point2D, Line, EPS, Segment, polar_sort 
from typing import List, Self, Tuple, Optional
import numpy as np


class Cluster:
    def __init__(self : Self, points: Optional[List[Point2D]] = None) -> None:
        self.points: List[Point2D] = points if points is not None else []
        polar_sort(self.points)
        self.seg: Optional[Segment] = None
        self.line: Optional[Line] = None

    def add_point(self : Self, p : Point2D) -> None:
        self.points.append(p)

    def orthogonal_regression_line(self : Self) -> "Line":
        if len(self.points) < 2:
            raise ValueError("At least two points are required")

        arr = np.array([p.as_tuple() for p in self.points], dtype=float)

        mean = arr.mean(axis=0)
        centered = arr - mean

        U, S, Vt = np.linalg.svd(centered, full_matrices=False)
        dx, dy = Vt[0]

        normal = np.array([-dy, dx], dtype=float)
        norm_len = np.linalg.norm(normal)
        if norm_len <= EPS:
            raise ValueError("Cannot determine a unique regression line")

        normal /= norm_len
        A, B = normal
        x0, y0 = mean
        C = -(A * x0 + B * y0)

        return Line(A, B, C)

    def leading_line(self : Self):
        if self.line == None:
            self.line = self.orthogonal_regression_line()
        return self.line

    def segment(self : Self):
        if self.seg == None:
            self.seg = self.approximating_segment()
        return self.seg

    def furthest_point(self : Self, line : Line) -> Tuple[int, float]:
        if not self.points:
            raise ValueError("No points provided")
        pos = 0
        maxd = line.distance(self.points[pos])
        for i in range(len(self.points)):
            curd = line.distance(self.points[i])
            if curd > maxd:
                pos = i
                maxd = curd
        return [pos, maxd]


    def approximating_segment(self: Self) -> Segment:
        if len(self.points) == 1:
            return Segment(self.points[0], self.points[0])
        line = self.leading_line()

        A, B, _ = line.A, line.B, line.C
        dirx, diry = B, -A

        p0 = line.project_point(self.points[0])
        t0 = p0.x * dirx + p0.y * diry
        min_p = max_p = p0
        min_t = max_t = t0

        for p in self.points[1:]:
            q = line.project_point(p)
            t = q.x * dirx + q.y * diry
            if t < min_t:
                min_t = t
                min_p = q
            if t > max_t:
                max_t = t
                max_p = q

        return Segment(min_p, max_p)
