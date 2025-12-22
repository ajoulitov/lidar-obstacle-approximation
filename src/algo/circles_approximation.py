from typing import List
from geom_core import Point2D, Segment, Circle, EPS
import math

def bounding_circle(seg: Segment, r_d: float) -> Circle:
    l = seg.length()
    mid = seg.midpoint()

    if l <= EPS:
        return Circle(mid, max(0.0, r_d))

    r = l / math.sqrt(3.0)
    d = seg.direction()
    n = Point2D(d.y, -d.x)
    n_len = math.hypot(n.x, n.y)
    if n_len <= EPS:
        return Circle(mid, r + r_d)

    n = n.scale(1.0 / n_len)
    to0 = Point2D(-mid.x, -mid.y)
    if n.dot(to0) < 0.0:
        n = n.scale(-1.0)

    center = mid + n.scale(-r)

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
                mid = base.midpoint()
                d = out[i].center.distance_to(out[j].center)
                r0 = d / math.sqrt(3.0)
                c = Circle(mid, r0 + max(out[i].radius, out[j].radius))

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

