from geom_core import Point2D, Segment
from typing import List
from .cluster import Cluster
from .segmentation import merge_all_segments
from .grouping import group_and_split

PARAMS = dict(
    d_group=0.1,
    d_split=0.01,
    d_merge=0.03,
    d_spread=0.01,
    d_p=0.0,
    N_min=2,
)

def approximate_with_egments(points : List[Point2D]) -> List[Segment]:
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