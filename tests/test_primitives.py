import math
from geom_core.primitives import Point2D


def test_arithmetic_and_dot_cross_norm():
    a = Point2D(1.0, 2.0)
    b = Point2D(3.0, 4.0)
    assert a + b == Point2D(4.0, 6.0)
    assert a - b == Point2D(-2.0, -2.0)
    assert abs(a.dot(b) - 11.0) < 1e-12
    assert abs(a.cross(b) - (1.0 * 4.0 - 2.0 * 3.0)) < 1e-12
    assert abs(a.norm() - math.hypot(1.0, 2.0)) < 1e-12

    n = a.normalized()
    assert abs(n.norm() - 1.0) < 1e-12


def test_rotate_and_as_tuple():
    p = Point2D(1.0, 0.0)
    r = p.rotate(math.pi / 2)
    assert abs(r.x - 0.0) < 1e-9
    assert abs(r.y - 1.0) < 1e-9
    assert isinstance(p.as_tuple(), tuple)
