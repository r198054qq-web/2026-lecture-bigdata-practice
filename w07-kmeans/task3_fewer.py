#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    """K-means accelerated using centroid-distance bounds."""

    def __init__(self, k, max_iter=50):
        self.k = k
        self.max_iter = max_iter
        self.iterations = 0

    def run(self, points, initial_centroids, distance):
        n = len(points)
        k = self.k
        centroids = list(initial_centroids)
        labels = [None] * n

        # Upper bounds on distances to assigned centroids.
        upper = [float("inf")] * n

        for iteration in range(1, self.max_iter + 1):
            self.iterations = iteration
            changed = False

            # Half the minimum distance to another centroid.
            separation = [float("inf")] * k

            if k > 1:
                for a in range(k):
                    for b in range(a + 1, k):
                        d = distance(centroids[a], centroids[b]) / 2
                        separation[a] = min(separation[a], d)
                        separation[b] = min(separation[b], d)

            for i, p in enumerate(points):
                old_label = labels[i]

                # Skip if the point is provably closest
                # to its previously assigned centroid.
                if old_label is not None:
                    if upper[i] < separation[old_label]:
                        continue

                best = None
                best_index = 0

                for j, c in enumerate(centroids):
                    d = distance(p, c)

                    if best is None or d < best - 1e-12:
                        best = d
                        best_index = j

                if labels[i] != best_index:
                    labels[i] = best_index
                    changed = True

                upper[i] = best

            old_centroids = centroids
            centroids = _means(
                points, labels, k, old_centroids
            )

            if not changed:
                break

            # Account for centroid movement.
            movement = [
                distance(old_centroids[j], centroids[j])
                for j in range(k)
            ]

            for i in range(n):
                upper[i] += movement[labels[i]]

        return labels, centroids
