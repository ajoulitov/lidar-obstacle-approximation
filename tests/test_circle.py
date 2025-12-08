from geom_core.primitives import Point2D
from geom_core.circle import Circle
from geom_core.line import Line
from geom_core.segment import Segment
import math


def test_circle_circle_intersections_two_points():
    c1 = Circle(center=Point2D(0.0, 0.0), radius=1.0)
    c2 = Circle(center=Point2D(1.0, 0.0), radius=1.0)
    pts = c1.intersection_points_with_circle(c2)
    assert pts is not None
    assert len(pts) == 2
    x_vals = {round(p.x, 6) for p in pts}
    assert round(0.5, 6) in x_vals
    y_vals = {round(abs(p.y), 6) for p in pts}
    assert round(math.sqrt(3.0) / 2.0, 6) in y_vals


def test_circle_circle_tangent():
    c1 = Circle(center=Point2D(0.0, 0.0), radius=1.0)
    c2 = Circle(center=Point2D(2.0, 0.0), radius=1.0)
    pts = c1.intersection_points_with_circle(c2)
    assert pts == [Point2D(1.0, 0.0)] or (isinstance(pts, list) and len(pts) == 1)


def test_circle_line_and_segment_intersections():
    c = Circle(center=Point2D(0.0, 1.0), radius=1.0)
    l = Line.from_two_points(Point2D(-1.0, 0.0), Point2D(1.0, 0.0))
    pts = c.intersection_points_with_line(l)
    assert len(pts) == 1
    assert abs(pts[0].x - 0.0) < 1e-12 and abs(pts[0].y - 0.0) < 1e-12

    seg = Segment(Point2D(-2.0, 0.0), Point2D(2.0, 0.0))
    pts_seg = Circle(center=Point2D(0.0, 0.0), radius=1.0).intersection_points_with_segment(seg)
    assert isinstance(pts_seg, list)
    assert len(pts_seg) == 2
    xs = {round(p.x, 6) for p in pts_seg}
    assert round(-1.0, 6) in xs and round(1.0, 6) in xs
