from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .primitives import Point2D, EPS
import math


@dataclass(frozen=True)
class Line:
    A: float
    B: float
    C: float

    @staticmethod
    def from_two_points(p1: Point2D, p2: Point2D) -> "Line":
        if abs(p1.x - p2.x) < EPS and abs(p1.y - p2.y) < EPS:
            raise ValueError("Two distinct points required to define a line.")
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        A = -dy
        B = dx
        norm = math.hypot(A, B)
        if norm <= EPS:
            raise ValueError("Degenerate normal vector")
        A /= norm
        B /= norm
        C = -(A * p1.x + B * p1.y)
        return Line(A, B, C)

    @staticmethod
    def from_point_direction(point: Point2D, direction: Point2D) -> "Line":
        if abs(direction.x) < EPS and abs(direction.y) < EPS:
            raise ValueError("Vector must be non-zero")
        A = -direction.y
        B = direction.x
        norm = math.hypot(A, B)
        A /= norm
        B /= norm
        C = -(A * point.x + B * point.y)
        return Line(A, B, C)

    def signed_distance(self, p: Point2D) -> float:
        return self.A * p.x + self.B * p.y + self.C

    def distance(self, p: Point2D) -> float:
        return abs(self.signed_distance(p))

    def project_point(self, p: Point2D) -> Point2D:
        d = self.signed_distance(p)
        return Point2D(p.x - d * self.A, p.y - d * self.B)

    def direction_vector(self) -> Point2D:
        return Point2D(-self.B, self.A)

    def intersection_with_line(self, other: "Line") -> Optional[Point2D]:
        det = self.A * other.B - other.A * self.B
        if abs(det) < EPS:
            return None
        x = (self.B * other.C - other.B * self.C) / det
        y = (other.A * self.C - self.A * other.C) / det
        return Point2D(x, y)

    def __repr__(self) -> str:
        return f"Line(A={self.A:.6g}, B={self.B:.6g}, C={self.C:.6g})"
