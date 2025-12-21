from typing import List
from .cluster import Cluster
from geom_core import Point2D
import sys

def group(c: Cluster, d_group: float = 1.0, d_p: float = 0.1) -> List[Cluster]:
    if not c.points:
        return []

    ans: List[Cluster] = [Cluster([c.points[0]])]
    for i in range(1, len(c.points)):
        if c.points[i].distance_to(c.points[i - 1]) < d_group + c.points[i].norm() * d_p:
            ans[-1].add_point(c.points[i])
        else:
            ans.append(Cluster([c.points[i]]))
    return ans


def split(c: Cluster, d_split: float = 1.0, d_p: float = 0.1, N_min: int = 2) -> List[Cluster]:
    if len(c.points) <= N_min:
        return [c]

    line = c.leading_line()
    mid, d = c.furthest_point(line)

    if d <= d_split + c.points[mid].norm() * d_p:
        return [c]

    if mid == 0 or mid == len(c.points) - 1:
        return [c]

    left = Cluster(c.points[:mid + 1])
    right = Cluster(c.points[mid:])
    return split(left, d_split, d_p, N_min) + split(right, d_split, d_p, N_min)


def group_and_split(points: List[Point2D],
                    d_group: float = 1.0, d_p: float = 0.1,
                    d_split: float = 1.0, N_min: int = 2) -> List[Cluster]:
    raw = group(Cluster(points), d_group=d_group, d_p=d_p)
    out: List[Cluster] = []
    sys.setrecursionlimit(1000)
    for cl in raw:
        out.extend(split(cl, d_split=d_split, d_p=d_p, N_min=N_min))
    return out
