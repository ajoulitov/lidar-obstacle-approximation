from __future__ import annotations
from typing import Tuple, List
from .primitives import Point2D, EPS
from .segment import Segment
from math import atan2

def closest_points_between_segments(s1: Segment, s2: Segment) -> Tuple[Point2D, Point2D]:
    p1 = s1.p1
    q1 = s2.p1
    u = s1.p2 - s1.p1
    v = s2.p2 - s2.p1
    w0 = p1 - q1

    a = u.dot(u)
    b = u.dot(v)
    c = v.dot(v)
    d = u.dot(w0)
    e = v.dot(w0)
    denom = a * c - b * b

    if denom > EPS:
        s = (b * e - c * d) / denom
        t = (a * e - b * d) / denom
    else:
        s = 0.0
        t = e / c if c > EPS else 0.0

    s_clamped = max(0.0, min(1.0, s))
    t_clamped = max(0.0, min(1.0, t))

    def clamp_and_refine(s_try: float, t_try: float) -> Tuple[float, float]:
        s_val = s_try
        t_val = t_try
        if s_val <= 0.0:
            s_val = 0.0
            t_val = e / c if c > EPS else 0.0
        elif s_val >= 1.0:
            s_val = 1.0
            t_val = (b + e) / c if c > EPS else 0.0

        if t_val <= 0.0:
            t_val = 0.0
            s_val = -d / a if a > EPS else 0.0
        elif t_val >= 1.0:
            t_val = 1.0
            s_val = (b - d) / a if a > EPS else 0.0

        s_val = max(0.0, min(1.0, s_val))
        t_val = max(0.0, min(1.0, t_val))
        return s_val, t_val

    s_final, t_final = clamp_and_refine(s_clamped, t_clamped)
    cp1 = Point2D(p1.x + u.x * s_final, p1.y + u.y * s_final)
    cp2 = Point2D(q1.x + v.x * t_final, q1.y + v.y * t_final)
    return cp1, cp2


def distance_between_segments(s1: Segment, s2: Segment) -> float:
    p, q = closest_points_between_segments(s1, s2)
    return p.distance_to(q)


def polar_angle(p: Point2D):
    dx = float(p.x)
    dy = float(p.y)
    ang = atan2(dy, dx)
    r2 = dx * dx + dy * dy
    return (ang, r2)


def polar_sort(points: List[Point2D]) -> List[Point2D]:

    points.sort(key=polar_angle)
