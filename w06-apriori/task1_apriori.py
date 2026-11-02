#!/usr/bin/env python3
"""Week 6 · Task 1 — A-Priori, and why the second pass is the whole problem.

Textbook §6.1 (market-basket model), §6.2 (A-Priori).

Finding frequent pairs is easy until you count how many pairs there are. With
n items there are n(n-1)/2 of them, and for a supermarket's 10,000 items that
is 50 million counters before you have read a single basket.

A-Priori's observation is one sentence long: **a pair cannot be frequent unless
both of its items are frequent.** One extra pass over the data buys you a much
smaller second pass, and the whole chapter is consequences of that trade.

    python3 task1_apriori.py --verify
"""
import argparse
from itertools import combinations

# Small enough to check by hand. support threshold 3 unless stated.
BASKETS = [
    {"bread", "milk"},
    {"bread", "diaper", "beer", "egg"},
    {"milk", "diaper", "beer", "cola"},
    {"bread", "milk", "diaper", "beer"},
    {"bread", "milk", "diaper", "cola"},
    {"bread", "milk", "beer"},
    {"diaper", "beer"},
]



def frequent_singletons(baskets, support):
    """Count frequent individual items."""
    counts = {}

    for basket in baskets:
        for item in basket:
            counts[item] = counts.get(item, 0) + 1

    return {
        item: count
        for item, count in counts.items()
        if count >= support
    }


def frequent_pairs(baskets, support):
    """Find frequent pairs using two-pass A-Priori."""

    # Pass 1: find frequent singletons.
    singles = frequent_singletons(baskets, support)
    frequent_items = set(singles)

    # Pass 2: count only pairs of frequent items.
    pair_counts = {}

    for basket in baskets:
        eligible = sorted(basket & frequent_items)

        for a, b in combinations(eligible, 2):
            pair = frozenset((a, b))
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

    return {
        pair: count
        for pair, count in pair_counts.items()
        if count >= support
    }


def association_rules(baskets, support, min_confidence):
    """Generate association rules with confidence and lift."""

    singles = frequent_singletons(baskets, support)
    pairs = frequent_pairs(baskets, support)

    total_baskets = len(baskets)
    rules = []

    if total_baskets == 0:
        return rules

    for pair, pair_count in pairs.items():
        a, b = sorted(pair)

        for antecedent, consequent in [(a, b), (b, a)]:
            confidence = pair_count / singles[antecedent]

            if confidence >= min_confidence:
                consequent_support = (
                    singles[consequent] / total_baskets
                )

                lift = confidence / consequent_support

                rules.append((
                    antecedent,
                    consequent,
                    confidence,
                    lift
                ))

    rules.sort(key=lambda rule: (-rule[2], rule[0], rule[1]))

    return rules


# ------------------------------------------------------------------- harness
def verify():
    fails = 0

    def check(label, got, want):
        nonlocal fails
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<44} {got}"
              + ("" if ok else f"\n{'':>54}want {want}"))
        fails += not ok

    try:
        singles = frequent_singletons(BASKETS, 3)
    except NotImplementedError:
        print("  frequent_singletons is still a stub"); return 1
    # counted by hand: bread 5, milk 5, diaper 5, beer 5, cola 2, egg 1
    check("frequent singletons at support 3",
          dict(sorted(singles.items())),
          {"beer": 5, "bread": 5, "diaper": 5, "milk": 5})

    try:
        pairs = frequent_pairs(BASKETS, 3)
    except NotImplementedError:
        print("  frequent_pairs is still a stub"); return 1
    got = {tuple(sorted(k)): v for k, v in pairs.items()}
    check("frequent pairs at support 3", dict(sorted(got.items())),
          {("beer", "bread"): 3, ("beer", "diaper"): 4, ("beer", "milk"): 3,
           ("bread", "diaper"): 3, ("bread", "milk"): 4, ("diaper", "milk"): 3})

    # cola appears twice, so it must never reach pass two
    check("infrequent items excluded from pairs",
          any("cola" in k or "egg" in k for k in got), False)

    try:
        rules = association_rules(BASKETS, 3, 0.75)
    except NotImplementedError:
        print("  association_rules is still a stub"); return 1
    # diaper -> beer: support 4, diaper 5, confidence 0.8
    hit = [r for r in rules if r[0] == "diaper" and r[1] == "beer"]
    check("diaper -> beer confidence", round(hit[0][2], 3) if hit else None, 0.8)
    check("rules are sorted by confidence",
          all(rules[i][2] >= rules[i + 1][2] for i in range(len(rules) - 1)), True)

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
