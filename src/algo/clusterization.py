from geom_core import Point2D, Segment, Circle
from typing import List, Tuple
from .cluster import Cluster
from .segmentation import merge_all_segments
from .grouping import group_and_split
from .circles_approximation import bounding_circle, merge_all_circles

PARAMS = dict(
    d_group=5,
    d_split=6,
    d_merge=15,
    d_spread=7,
    d_p=0,
    N_min=5,
    r_d=0,
    r_max=30,
)


def approximate_with_segments(points : List[Point2D]) -> List[Segment]:
    clusters = group_and_split(
        points,
        d_group=PARAMS["d_group"],
        d_p=PARAMS["d_p"],
        d_split=PARAMS["d_split"],
        N_min=PARAMS["N_min"],
    )
    merged = merge_all_segments(
        clusters,
        d_merge=PARAMS["d_merge"],
        d_spread=PARAMS["d_spread"],
    )
    segments = [c.approximating_segment() for c in merged]
    return segments


def approximate_with_circles(points: List[Point2D]) -> List[Circle]:
    segs = approximate_with_segments(points)
    out: List[Circle] = []
    for s in segs:
        c = bounding_circle(s, PARAMS["r_d"])
        if c.radius <= PARAMS["r_max"]:
            out.append(c)
    return merge_all_circles(out, r_max=PARAMS["r_max"])

def approximate(points: List[Point2D]) -> Tuple[List[Segment], List[Circle]]:
    segs = approximate_with_segments(points)
    circs = approximate_with_circles(points)
    return segs, circs