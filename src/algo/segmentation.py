from typing import List, Tuple
from .cluster import Cluster
from ..geom_core import distance_between_segments
from .dsu import DSU


def merge_two_segments(cluster_1: Cluster, cluster_2: Cluster,
                       d_merge: float = 0.1, d_spread: float = 0.5) -> List[Cluster]:
    seg_1 = cluster_1.segment()
    seg_2 = cluster_2.segment()

    if distance_between_segments(seg_1, seg_2) >= d_merge:
        return [cluster_1, cluster_2]

    merged_cluster = Cluster(cluster_1.points + cluster_2.points)
    merged_line = merged_cluster.leading_line()

    d1 = merged_line.distance(seg_1.p1)
    d2 = merged_line.distance(seg_1.p2)
    d3 = merged_line.distance(seg_2.p1)
    d4 = merged_line.distance(seg_2.p2)

    if max(d1, d2, d3, d4) >= d_spread:
        return [cluster_1, cluster_2]

    return [merged_cluster]


def merge_all_segments(clusters: List[Cluster],
                       d_merge: float = 0.1,
                       d_spread: float = 0.5) -> List[Cluster]:
    n = len(clusters)
    if n <= 1:
        return clusters

    dsu = DSU(n)
    comp_cluster: List[Cluster | None] = list(clusters)
    roots = set(range(n))

    queue: List[Tuple[int, int]] = [(i, j) for i in range(n) for j in range(i + 1, n)]
    qpos = 0

    while qpos < len(queue):
        a0, b0 = queue[qpos]
        qpos += 1

        a = dsu.get(a0)
        b = dsu.get(b0)
        if a == b:
            continue
        if a not in roots or b not in roots:
            continue

        ca = comp_cluster[a]
        cb = comp_cluster[b]
        if ca is None or cb is None:
            continue

        merged_list = merge_two_segments(ca, cb, d_merge=d_merge, d_spread=d_spread)

        if len(merged_list) == 1:
            merged_cluster = merged_list[0]

            dsu.merge(a, b)
            new_root = dsu.get(a)
            old_root = b if new_root == a else a

            comp_cluster[new_root] = merged_cluster
            comp_cluster[old_root] = None
            roots.discard(old_root)

            for r in list(roots):
                if r != new_root:
                    queue.append((new_root, r))

    return [comp_cluster[r] for r in roots if comp_cluster[r] is not None]
