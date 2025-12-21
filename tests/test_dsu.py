from algo import DSU

def test_dsu_get_initial():
    dsu = DSU(5)
    assert [dsu.get(i) for i in range(5)] == [0, 1, 2, 3, 4]


def test_dsu_merge_and_get():
    dsu = DSU(4)
    dsu.merge(0, 1)
    r0 = dsu.get(0)
    r1 = dsu.get(1)
    assert r0 == r1

    dsu.merge(2, 3)
    assert dsu.get(2) == dsu.get(3)
    assert dsu.get(0) != dsu.get(2)

    dsu.merge(0, 1)
    assert dsu.get(0) == dsu.get(1)
