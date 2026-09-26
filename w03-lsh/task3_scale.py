#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """Near-duplicate finder using MinHash + LSH."""

    def __init__(self, threshold):
        self.threshold = threshold

        # 120 hashes, split into 30 bands of 4 rows each.
        self.num_hashes = 120
        self.bands = 30

    def find(self, docs, similarity):
        import random

        if not docs:
            return set()

        # Prime larger than the shingle vocabulary.
        prime = 10007

        # Reproducible, independently generated hash parameters.
        rng = random.Random(12345)
        hashes = []

        for _ in range(self.num_hashes):
            a = rng.randrange(1, prime)
            b = rng.randrange(0, prime)
            hashes.append((a, b))

        # Build MinHash signatures.
        signatures = []

        for doc in docs:
            sig = []

            for a, b in hashes:
                minimum = prime

                for shingle in doc:
                    value = (a * shingle + b) % prime
                    if value < minimum:
                        minimum = value

                sig.append(minimum)

            signatures.append(sig)

        # LSH
        rows_per_band = self.num_hashes // self.bands
        candidates = set()

        for band in range(self.bands):
            buckets = {}

            start = band * rows_per_band
            end = start + rows_per_band

            for i, sig in enumerate(signatures):
                key = tuple(sig[start:end])
                buckets.setdefault(key, []).append(i)

            for bucket in buckets.values():
                if len(bucket) > 1:
                    for x in range(len(bucket)):
                        for y in range(x + 1, len(bucket)):
                            candidates.add((bucket[x], bucket[y]))

        # Exact similarity only for LSH candidates.
        out = set()

        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                out.add((i, j))

        return out