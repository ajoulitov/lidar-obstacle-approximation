from typing import List
from geom_core import Point2D, Segment, Circle, EPS
import math


def bounding_circle(seg: Segment, r_d: float) -> Circle:
    l = seg.length()
    if l <= EPS:
        return Circle(seg.midpoint(), r_d)

    r = l / math.sqrt(3.0)
    d = seg.direction()
    n = Point2D(d.y, -d.x)
    mid = seg.midpoint()
    to0 = Point2D(-mid.x, -mid.y)
    if n.dot(to0) < 0.0:
        n = n.scale(-1.0)
    center = mid + n.scale(r)
    return Circle(center, r + r_d)


def merge_all_circles(circles: List[Circle], r_max) -> List[Circle]:
    out = list(circles)
    changed = True
    while changed:
        changed = False
        n = len(out)
        rem = set()
        for i in range(n):
            if i in rem:
                continue
            for j in range(n):
                if i == j or j in rem:
                    continue
                if out[i].is_inside(out[j]):
                    rem.add(i)
                    break

        if rem:
            out = [out[i] for i in range(n) if i not in rem]
            changed = True
            continue

        n = len(out)
        merged = False
        for i in range(n):
            for j in range(i + 1, n):
                if not out[i].intersects_with_circle(out[j]):
                    continue
                base = Segment(out[i].center, out[j].center)
                c = bounding_circle(base, 0.0)
                c = Circle(c.center, c.radius + max(out[i].radius, out[j].radius))
                if c.radius > r_max:
                    continue
                out = [out[k] for k in range(n) if k != i and k != j]
                out.append(c)
                changed = True
                merged = True
                break

            if merged:
                break

    return out

