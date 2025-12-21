from geom_core import Point2D

from algo.cluster import Cluster
from algo.segmentation import merge_all_segments
from algo.clusterization import approximate_with_segments


def test_merging():
    c1 = Cluster([Point2D(0, 0), Point2D(1, 0)])
    c2 = Cluster([Point2D(1.05, 0), Point2D(2, 0)])
    c3 = Cluster([Point2D(10, 0), Point2D(11, 0)])
    out = merge_all_segments([c1, c2, c3], d_merge=0.2, d_spread=0.1)
    assert len(out) == 2


def test_all():
    pts = [
        Point2D(0, 0),
        Point2D(0.05, 0),
        Point2D(0.1, 0),
        Point2D(2, 0),
        Point2D(2.05, 0),
    ]
    segs = approximate_with_segments(pts)
    assert isinstance(segs, list)
