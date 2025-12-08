from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
from .primitives import Point2D, EPS
from .line import Line
from .segment import Segment
import math


@dataclass
class Circle:
    center: Point2D
    radius: float

    def contains_point(self, p: Point2D) -> bool:
        return self.center.distance_to(p) <= self.radius + EPS

    def is_inside(self, other: "Circle") -> bool:
        d = self.center.distance_to(other.center)
        return d + self.radius <= other.radius + EPS

    def intersects_with_circle(self, other: "Circle") -> bool:
        d = self.center.distance_to(other.center)
        if d > self.radius + other.radius + EPS:
            return False
        if d + min(self.radius, other.radius) < max(self.radius, other.radius) - EPS:
            return False
        return True

    def intersection_points_with_circle(self, other: "Circle") -> Optional[List[Point2D]]:
        d = self.center.distance_to(other.center)
        if d > self.radius + other.radius + EPS:
            return []
        if d < abs(self.radius - other.radius) - EPS:
            return []
        if d <= EPS and abs(self.radius - other.radius) <= EPS:
            return None

        a = (self.radius * self.radius - other.radius * other.radius + d * d) / (2.0 * d)
        h_sq = self.radius * self.radius - a * a
        if h_sq < -EPS:
            return []
        h = math.sqrt(max(0.0, h_sq))
        vx = (other.center.x - self.center.x) / d
        vy = (other.center.y - self.center.y) / d
        p2x = self.center.x + a * vx
        p2y = self.center.y + a * vy
        rx = -vy * h
        ry = vx * h
        p1 = Point2D(p2x + rx, p2y + ry)
        p2 = Point2D(p2x - rx, p2y - ry)
        if p1.distance_to(p2) <= 1e-12:
            return [p1]
        return [p1, p2]

    def intersection_points_with_line(self, line: Line) -> Optional[List[Point2D]]:
        proj = line.project_point(self.center)
        d = proj.distance_to(self.center)
        if d > self.radius + EPS:
            return []
        s = math.sqrt(max(0.0, self.radius * self.radius - d * d))
        dirv = line.direction_vector()
        dir_norm = math.hypot(dirv.x, dirv.y)
        if dir_norm <= EPS:
            return []
        ux = dirv.x / dir_norm
        uy = dirv.y / dir_norm
        p1 = Point2D(proj.x + ux * s, proj.y + uy * s)
        p2 = Point2D(proj.x - ux * s, proj.y - uy * s)
        if p1.distance_to(p2) <= 1e-12:
            return [p1]
        return [p1, p2]

    def intersection_points_with_segment(self, seg: Segment) -> Optional[List[Point2D]]:
        pts = self.intersection_points_with_line(seg.as_line())
        if pts is None:
            return None
        result: List[Point2D] = []
        for p in pts:
            if seg.contains_point_strict(p):
                result.append(p)
        return result

    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius:.6g})"
