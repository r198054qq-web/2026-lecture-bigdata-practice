# Task 2 - Memory and Runtime Limits

| Items | Exact Time (s) | Exact Memory (MB) | FM Time (s) |
|---|---:|---:|---:|
| 100000 | 0.27 | 3.9 | 51.74 |
| 200000 | 0.51 | 5.8 | 86.00 |
| 400000 | 1.14 | 11.6 | 196.20 |
| 1600000 | 5.95 | 46.6 | 768.66 |

## Memory Curve

Exact memory increased as the input size increased.
At 1,600,000 items, exact counting used 46.6 MB.

## Observation

Exact counting was faster than the Python FM implementation in these experiments.
The exact method did not run out of memory at the largest tested size.
The memory limit was not reached, but memory usage increased with data size.
