from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .primitives import Point2D, EPS
from .line import Line


@dataclass
class Segment:
    p1: Point2D
    p2: Point2D

    def __post_init__(self) -> None:
        pass

    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    def midpoint(self) -> Point2D:
        return Point2D((self.p1.x + self.p2.x) / 2.0, (self.p1.y + self.p2.y) / 2.0)

    def direction(self) -> Point2D:
        v = self.p2 - self.p1
        n = v.norm()
        if n <= EPS:
            return Point2D(0.0, 0.0)
        return Point2D(v.x / n, v.y / n)

    def as_line(self) -> Line:
        return Line.from_two_points(self.p1, self.p2)

    def contains_point_strict(self, p: Point2D) -> bool:
        v1 = p - self.p1
        v2 = self.p2 - self.p1
        if abs(v1.cross(v2)) > EPS:
            return False
        dot = v1.dot(v2)
        if dot < -EPS:
            return False
        if dot > v2.norm2() + EPS:
            return False
        return True

    def project_point_clamped(self, p: Point2D) -> Point2D:
        a = self.p1
        b = self.p2
        ab = b - a
        denom = ab.norm2()
        if denom <= EPS:
            return a
        t = (p - a).dot(ab) / denom
        if t <= 0.0:
            return a
        if t >= 1.0:
            return b
        return Point2D(a.x + ab.x * t, a.y + ab.y * t)

    def distance_to_point(self, p: Point2D) -> float:
        proj = self.project_point_clamped(p)
        return proj.distance_to(p)

    def intersects_with_segment(self, other: "Segment") -> bool:
        def orient(a: Point2D, b: Point2D, c: Point2D) -> float:
            return (b - a).cross(c - a)

        a1, a2 = self.p1, self.p2
        b1, b2 = other.p1, other.p2

        o1 = orient(a1, a2, b1)
        o2 = orient(a1, a2, b2)
        o3 = orient(b1, b2, a1)
        o4 = orient(b1, b2, a2)

        if (o1 * o2 < -EPS) and (o3 * o4 < -EPS):
            return True

        if abs(o1) <= EPS and Segment(a1, a2).contains_point_strict(b1):
            return True
        if abs(o2) <= EPS and Segment(a1, a2).contains_point_strict(b2):
            return True
        if abs(o3) <= EPS and Segment(b1, b2).contains_point_strict(a1):
            return True
        if abs(o4) <= EPS and Segment(b1, b2).contains_point_strict(a2):
            return True

        return False

    def intersection_point_with_segment(self, other: "Segment") -> Optional[Point2D]:
        if not self.intersects_with_segment(other):
            return None
        l1 = self.as_line()
        l2 = other.as_line()
        ip = l1.intersection_with_line(l2)
        if ip is None:
            return None
        if self.contains_point_strict(ip) and other.contains_point_strict(ip):
            return ip
        p1 = self.project_point_clamped(ip)
        p2 = other.project_point_clamped(ip)
        if p1.distance_to(p2) <= 1e-6:
            return Point2D((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)
        return None

    def __repr__(self) -> str:
        return f"Segment(p1={self.p1}, p2={self.p2})"
