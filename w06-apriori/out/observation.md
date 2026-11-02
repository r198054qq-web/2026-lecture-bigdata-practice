# Week 06 — Observations

## Task 1 — A-Priori

A-Priori first identifies frequent individual items and then counts only pairs containing two frequent items. This reduces the number of candidate pairs without losing any frequent pairs. Association rules use confidence and lift to measure the strength of relationships between items.

## Task 2 — Support Threshold Explosion

Reducing support from 400 to 6 increased frequent pairs from 249 to 101,938. Peak candidate counters increased to 893,456, while peak memory reached 119.4 MB. No memory limit was reached in the tested range.

## Task 3 — PCY

PCY reduced peak pair counters from 820,259 to 54,615, a 93.3% reduction, while finding exactly the same 6,397 frequent pairs. Its runtime increased from 1.50 to 6.40 seconds because of additional hashing work.

The bucket counts are needed only during the first pass. Before the second pass, they are converted into a compact bitmap and the original bucket-count array is released. This reduces memory usage during pair counting, although the bitmap and candidate counters still occupy memory.