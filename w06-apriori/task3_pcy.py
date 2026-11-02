#!/usr/bin/env python3
"""Week 6 · Task 3 — Make pass two fit.

Textbook §6.3 (PCY), §6.3.2 - §6.3.4.

`PlainApriori` does what Task 1 asked: use pass one to drop infrequent items,
then count every pair of surviving items. That is already much better than
counting all pairs. It is still not enough, because the surviving items are the
common ones, and the common ones appear together constantly.

The harness measures **the peak number of pair counters you held**, because
that is the thing that decides whether the algorithm runs at all. §6.3 is about
spending pass one's spare memory to shrink it.

    python3 bench.py
    python3 bench.py --yours

Correctness first: you must find exactly the same frequent pairs. Finding fewer
is not an optimisation.
"""
from collections import Counter
from itertools import combinations


class PlainApriori:
    """Pass one drops infrequent items. Pass two counts every surviving pair."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()
        for basket in baskets:
            counts.update(basket)
        frequent = {i for i, c in counts.items() if c >= self.support}

        pair_counts = Counter()
        for basket in baskets:
            items = sorted(basket & frequent)
            for pair in combinations(items, 2):
                pair_counts[pair] += 1
            self.peak_counters = max(self.peak_counters, len(pair_counts))

        return {frozenset(p): c for p, c in pair_counts.items()
                if c >= self.support}



class YourAlgorithm:
    """PCY algorithm using hash buckets to filter candidate pairs."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0
        self.num_buckets = 200003

    def _bucket(self, a, b):
        """Deterministic hash for an unordered pair."""
        import hashlib

        data = (str(a) + "\0" + str(b)).encode("utf-8")
        digest = hashlib.blake2b(
            data, digest_size=8
        ).digest()

        return int.from_bytes(digest, "big") % self.num_buckets

    def run(self, baskets):
        # Pass 1: count items and hash all observed pairs.
        item_counts = Counter()
        bucket_counts = [0] * self.num_buckets

        for basket in baskets:
            item_counts.update(basket)

            items = sorted(basket)
            for a, b in combinations(items, 2):
                bucket_counts[self._bucket(a, b)] += 1

        # Identify frequent individual items.
        frequent = {
            item for item, count in item_counts.items()
            if count >= self.support
        }

        # Compress bucket counts into a bitmap.
        bitmap = bytearray((self.num_buckets + 7) // 8)

        for index, count in enumerate(bucket_counts):
            if count >= self.support:
                bitmap[index // 8] |= 1 << (index % 8)

        # Release the full bucket counters before pass 2.
        del bucket_counts
        del item_counts

        # Pass 2: count only pairs passing both filters.
        pair_counts = Counter()
        self.peak_counters = 0

        for basket in baskets:
            items = sorted(basket & frequent)

            for a, b in combinations(items, 2):
                index = self._bucket(a, b)

                if bitmap[index // 8] & (1 << (index % 8)):
                    pair_counts[(a, b)] += 1

            self.peak_counters = max(
                self.peak_counters,
                len(pair_counts)
            )

        return {
            frozenset(pair): count
            for pair, count in pair_counts.items()
            if count >= self.support
        }
