from geom_core.primitives import Point2D
from geom_core.line import Line


def test_line_from_two_points_and_projection():
    p1 = Point2D(0.0, 0.0)
    p2 = Point2D(1.0, 0.0)
    line = Line.from_two_points(p1, p2)

    pt = Point2D(0.0, 1.0)
    assert abs(line.signed_distance(pt) - 1.0) < 1e-12
    proj = line.project_point(pt)
    assert abs(proj.x - 0.0) < 1e-12 and abs(proj.y - 0.0) < 1e-12


def test_line_intersection():
    lx = Line.from_two_points(Point2D(0.0, 0.0), Point2D(1.0, 0.0))
    ly = Line.from_two_points(Point2D(0.0, 0.0), Point2D(0.0, 1.0))
    ip = lx.intersection_with_line(ly)
    assert ip is not None
    assert abs(ip.x - 0.0) < 1e-12 and abs(ip.y - 0.0) < 1e-12
