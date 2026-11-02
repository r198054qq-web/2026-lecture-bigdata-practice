
#!/usr/bin/env python3
"""Week 7 - Task 1: k-means clustering."""

import argparse
import math
import random

BLOBS = [
    (0.0, 0.0), (0.2, 0.1), (0.1, 0.2),
    (8.0, 8.0), (8.2, 8.1), (8.1, 8.2),
    (0.0, 8.0), (0.2, 8.1), (0.1, 8.2)
]


def euclidean(a, b):
    """Euclidean distance in any number of dimensions."""
    if len(a) != len(b):
        raise ValueError("Points must have the same dimension")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def assign(points, centroids):
    """Assign each point to its nearest centroid."""
    return [
        min(
            range(len(centroids)),
            key=lambda i: euclidean(p, centroids[i])
        )
        for p in points
    ]


def update(points, labels, k):
    """Calculate new means; return None for empty clusters."""
    if not points:
        raise ValueError("Points cannot be empty")

    dim = len(points[0])
    groups = [[] for _ in range(k)]

    for p, label in zip(points, labels):
        groups[label].append(p)

    result = []
    for group in groups:
        if not group:
            result.append(None)
        else:
            mean = tuple(
                sum(p[d] for p in group) / len(group)
                for d in range(dim)
            )
            result.append(mean)

    return result


def sse_of(points, labels, centroids):
    """Sum of squared errors."""
    return sum(
        euclidean(p, centroids[label]) ** 2
        for p, label in zip(points, labels)
    )


def kmeans(points, k, init="random", seed=246, max_iter=100):
    """Run k-means and return labels, centroids, SSE."""
    if not 1 <= k <= len(points):
        raise ValueError("k must be between 1 and number of points")

    rng = random.Random(seed)

    if init == "random":
        centroids = list(rng.sample(points, k))

    elif init == "++":
        centroids = [rng.choice(points)]

        while len(centroids) < k:
            weights = [
                min(euclidean(p, c) ** 2 for c in centroids)
                for p in points
            ]

            if sum(weights) == 0:
                remaining = [p for p in points if p not in centroids]
                centroids.append(
                    rng.choice(remaining if remaining else points)
                )
            else:
                centroids.append(
                    rng.choices(points, weights=weights, k=1)[0]
                )
    else:
        raise ValueError("Unknown initialization method")

    kmeans.iterations = 0

    for i in range(max_iter):
        labels = assign(points, centroids)
        new_centroids = update(points, labels, k)

        # Keep the previous centroid for an empty cluster.
        new_centroids = [
            old if new is None else new
            for old, new in zip(centroids, new_centroids)
        ]

        kmeans.iterations = i + 1

        if new_centroids == centroids:
            break

        centroids = new_centroids

    labels = assign(points, centroids)
    sse = sse_of(points, labels, centroids)

    return labels, centroids, sse


# Verification tests provided by the instructor.
def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<50} {detail}")
        fails += not ok

    check("distance in 2d",
          abs(euclidean((0, 0), (3, 4)) - 5) < 1e-9)

    check("distance in 5d",
          abs(euclidean((0,) * 5, (1,) * 5) - math.sqrt(5)) < 1e-9)

    labels, cents, sse = kmeans(BLOBS, 3, init="++", seed=1)

    groups = {}
    for p, label in zip(BLOBS, labels):
        groups.setdefault(label, []).append(p)

    check("three clusters of three",
          sorted(len(g) for g in groups.values()) == [3, 3, 3],
          sorted(len(g) for g in groups.values()))

    check("the three blobs were recovered",
          all(
              max(q[0] for q in g) - min(q[0] for q in g) < 1
              and max(q[1] for q in g) - min(q[1] for q in g) < 1
              for g in groups.values()
          ))

    check("sse is small when clusters are right",
          sse < 1.0, f"sse {sse:.4f}")

    randoms = [
        kmeans(BLOBS, 3, init="random", seed=s)[2]
        for s in range(40)
    ]

    plusplus = [
        kmeans(BLOBS, 3, init="++", seed=s)[2]
        for s in range(40)
    ]

    check("random init sometimes lands badly",
          max(randoms) > min(randoms) * 5,
          f"sse from {min(randoms):.3f} to {max(randoms):.3f}")

    check("k-means++ is more reliable than random",
          sum(plusplus) / len(plusplus)
          <= sum(randoms) / len(randoms),
          f"mean sse: ++ {sum(plusplus)/40:.3f} vs "
          f"random {sum(randoms)/40:.3f}")

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    raise SystemExit(
        verify() if args.verify else parser.print_help()
    )
