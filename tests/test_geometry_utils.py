from geom_core.primitives import Point2D
from geom_core.segment import Segment
from geom_core.geometry_utils import closest_points_between_segments, distance_between_segments


def test_closest_points_parallel_segments():
    s1 = Segment(Point2D(0.0, 0.0), Point2D(1.0, 0.0))
    s2 = Segment(Point2D(0.0, 1.0), Point2D(1.0, 1.0))
    p, q = closest_points_between_segments(s1, s2)
    d = p.distance_to(q)
    assert abs(d - 1.0) < 1e-9


def test_closest_points_intersecting_segments_zero_distance():
    s1 = Segment(Point2D(0.0, 0.0), Point2D(1.0, 1.0))
    s2 = Segment(Point2D(0.0, 1.0), Point2D(1.0, 0.0))
    p, q = closest_points_between_segments(s1, s2)
    assert abs(p.distance_to(q)) < 1e-9
    assert abs(distance_between_segments(s1, s2)) < 1e-9
