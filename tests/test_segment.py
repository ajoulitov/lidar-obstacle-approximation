from geom_core.primitives import Point2D
from geom_core.segment import Segment


def test_segment_basic_ops_and_projection():
    s = Segment(Point2D(0.0, 0.0), Point2D(1.0, 0.0))
    assert abs(s.length() - 1.0) < 1e-12
    mid = s.midpoint()
    assert mid == Point2D(0.5, 0.0)

    p_right = Point2D(2.0, 0.0)
    proj_r = s.project_point_clamped(p_right)
    assert proj_r == Point2D(1.0, 0.0)

    p_left = Point2D(-1.0, 0.0)
    proj_l = s.project_point_clamped(p_left)
    assert proj_l == Point2D(0.0, 0.0)

    p_above = Point2D(0.5, 0.5)
    proj_above = s.project_point_clamped(p_above)
    assert abs(proj_above.x - 0.5) < 1e-12 and abs(proj_above.y - 0.0) < 1e-12

    assert s.contains_point_strict(Point2D(0.5, 0.0))
    assert not s.contains_point_strict(Point2D(1.1, 0.0))


def test_segment_intersections():
    s1 = Segment(Point2D(0.0, 0.0), Point2D(1.0, 1.0))
    s2 = Segment(Point2D(0.0, 1.0), Point2D(1.0, 0.0))
    assert s1.intersects_with_segment(s2)
    ip = s1.intersection_point_with_segment(s2)
    assert ip is not None
    assert abs(ip.x - 0.5) < 1e-12 and abs(ip.y - 0.5) < 1e-12

    a = Segment(Point2D(0.0, 0.0), Point2D(1.0, 0.0))
    b = Segment(Point2D(1.0, 0.0), Point2D(2.0, 0.0))
    assert a.intersects_with_segment(b)
    c = Segment(Point2D(0.0, 0.0), Point2D(2.0, 0.0))
    d = Segment(Point2D(1.0, 0.0), Point2D(3.0, 0.0))
    assert c.intersects_with_segment(d)
