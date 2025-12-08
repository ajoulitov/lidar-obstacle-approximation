from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Tuple

EPS: float = 1e-9


@dataclass(frozen=True)
class Point2D:
    x: float
    y: float

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        return Point2D(self.x - other.x, self.y - other.y)

    def scale(self, s: float) -> Point2D:
        return Point2D(self.x * s, self.y * s)

    def dot(self, other: Point2D) -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Point2D) -> float:
        return self.x * other.y - self.y * other.x

    def norm(self) -> float:
        return math.hypot(self.x, self.y)

    def norm2(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalized(self) -> Point2D:
        n = self.norm()
        if n <= EPS:
            raise ValueError("Cannot normalize zero vector")
        return Point2D(self.x / n, self.y / n)

    def distance_to(self, other: Point2D) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def rotate(self, angle_rad: float, origin: "Point2D | None" = None) -> Point2D:
        if origin is None:
            ox, oy = 0.0, 0.0
        else:
            ox, oy = origin.x, origin.y
        px = self.x - ox
        py = self.y - oy
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        rx = px * c - py * s
        ry = px * s + py * c
        return Point2D(rx + ox, ry + oy)

    def as_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Point2D(x={self.x:.6g}, y={self.y:.6g})"
