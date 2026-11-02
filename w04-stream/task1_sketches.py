#!/usr/bin/env python3
"""Week 4 · Task 1 — Stream sketches."""

import argparse
import random
import hashlib
import math
import statistics


class BloomFilter:
    """Membership test with one-sided error."""

    def __init__(self, m, k, seed=246):
        self.m = m
        self.k = k
        self.seed = seed

        # m bits. Using a bytearray keeps the memory bounded.
        self.bits = bytearray((m + 7) // 8)

    def _hashes(self, item):
        """Generate k deterministic bit positions."""
        data = str(item).encode("utf-8")

        for i in range(self.k):
            h = hashlib.sha256(
                f"{self.seed}:{i}:".encode("utf-8") + data
            ).digest()

            value = int.from_bytes(h[:8], "big")
            yield value % self.m

    def add(self, item):
        for pos in self._hashes(item):
            byte_index = pos // 8
            bit_index = pos % 8
            self.bits[byte_index] |= 1 << bit_index

    def __contains__(self, item):
        for pos in self._hashes(item):
            byte_index = pos // 8
            bit_index = pos % 8

            if not (self.bits[byte_index] & (1 << bit_index)):
                return False

        return True

    def expected_fp_rate(self, n_inserted):
        """Textbook Bloom-filter false-positive probability."""
        return (1 - math.exp(-self.k * n_inserted / self.m)) ** self.k


def flajolet_martin(stream, n_hashes=64, seed=246):
    """Estimate the number of distinct elements using Flajolet-Martin."""

    max_zeros = [0] * n_hashes

    for item in stream:
        data = str(item).encode("utf-8")

        for i in range(n_hashes):
            digest = hashlib.sha256(
                f"{seed}:{i}:".encode("utf-8") + data
            ).digest()

            value = int.from_bytes(digest[:8], "big")

            if value == 0:
                zeros = 64
            else:
                zeros = (value & -value).bit_length() - 1

            if zeros > max_zeros[i]:
                max_zeros[i] = zeros

    # Group the hashes, take a median inside each group,
    # then average the group estimates.
    group_size = 8
    group_estimates = []

    for start in range(0, n_hashes, group_size):
        group = max_zeros[start:start + group_size]

        if not group:
            continue

        group_r = statistics.median(group)
        group_estimates.append(2.0 ** group_r)

    if not group_estimates:
        return 0.0

    return float(sum(group_estimates) / len(group_estimates))


def reservoir_sample(stream, k, seed=246):
    """Uniform reservoir sampling for a stream of unknown length."""

    if k <= 0:
        return []

    rng = random.Random(seed)
    reservoir = []

    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            # At stream position i, choose uniformly from 0 ... i.
            j = rng.randrange(i + 1)

            if j < k:
                reservoir[j] = item

    return reservoir


# ------------------------------------------------------------------- harness
def verify():
    fails = 0
    rng = random.Random(246)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<46} {detail}")
        fails += not ok

    # --- Bloom: no false negatives, ever
    try:
        bf = BloomFilter(m=8192, k=5)
    except NotImplementedError:
        print("  BloomFilter is still a stub")
        return 1

    inserted = [f"item-{i}" for i in range(800)]

    for x in inserted:
        bf.add(x)

    check("no false negatives", all(x in bf for x in inserted))

    absent = [f"other-{i}" for i in range(20_000)]
    fp = sum(1 for x in absent if x in bf) / len(absent)

    predicted = bf.expected_fp_rate(len(inserted))

    close = abs(fp - predicted) < max(0.02, predicted * 0.5)

    check(
        "measured false-positive rate matches theory",
        close,
        f"measured {fp:.3%}, predicted {predicted:.3%}",
    )

    # --- Flajolet-Martin
    try:
        distinct = 20_000
        stream = [
            f"k{rng.randrange(distinct)}"
            for _ in range(120_000)
        ]

        est = flajolet_martin(stream)

    except NotImplementedError:
        print("  flajolet_martin is still a stub")
        return 1

    true_distinct = len(set(stream))
    ratio = est / true_distinct

    check(
        "distinct estimate within a factor of 2",
        0.5 <= ratio <= 2.0,
        f"estimated {est:,.0f}, true {true_distinct:,} ({ratio:.2f}x)",
    )

    # --- Reservoir
    try:
        counts = [0] * 20
        trials = 4000

        for t in range(trials):
            s = reservoir_sample(range(20), 5, seed=t)

            for i in s:
                counts[i] += 1

    except NotImplementedError:
        print("  reservoir_sample is still a stub")
        return 1

    expected = trials * 5 / 20

    spread = (max(counts) - min(counts)) / expected

    check(
        "reservoir is uniform across items",
        spread < 0.15,
        f"spread {spread:.1%} around {expected:.0f}",
    )

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")

    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()

    raise SystemExit(
        verify() if a.verify else p.print_help()
    )