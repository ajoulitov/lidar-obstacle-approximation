from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .primitives import Point2D, EPS


@dataclass
class AABB:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    @staticmethod
    def from_points(points: List[Point2D]) -> "AABB":
        if not points:
            raise ValueError("Empty point set")
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        return AABB(min(xs), min(ys), max(xs), max(ys))

    def contains_point(self, p: Point2D) -> bool:
        return (self.xmin - EPS <= p.x <= self.xmax + EPS) and (self.ymin - EPS <= p.y <= self.ymax + EPS)

    def expand(self, margin: float) -> "AABB":
        return AABB(self.xmin - margin, self.ymin - margin, self.xmax + margin, self.ymax + margin)

    def __repr__(self) -> str:
        return f"AABB(xmin={self.xmin:.6g}, ymin={self.ymin:.6g}, xmax={self.xmax:.6g}, ymax={self.ymax:.6g})"
