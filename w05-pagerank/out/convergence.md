# Task 2 - PageRank Convergence

## Experiment 1: Effect of Beta

| Beta | Iterations | Time (s) |
|---|---:|---:|
| 0.50 | 14 | 0.009 |
| 0.70 | 17 | 0.011 |
| 0.85 | 20 | 0.013 |
| 0.95 | 23 | 0.016 |
| 0.99 | 24 | 0.015 |

As beta increases, PageRank generally needs more iterations to converge.

## Experiment 2: Graph Size

| Beta | Nodes | Iterations | Time (s) |
|---|---:|---:|---:|
| 0.85 | 1200 | 20 | 0.013 |
| 0.85 | 20000 | 21 | 0.306 |
| 0.95 | 1200 | 23 | 0.016 |
| 0.95 | 20000 | 24 | 0.414 |

Larger graphs required more computation time, while the iteration count increased only slightly.

## Experiment 3: Tolerance

| Tolerance | Beta | Iterations |
|---|---:|---:|
| 1e-6 | 0.85 | 12 |
| 1e-10 | 0.85 | 20 |
| 1e-12 | 0.85 | 25 |

A stricter convergence tolerance requires more iterations.

## Conclusion

Convergence depends on beta, graph structure, and tolerance. Higher beta and stricter tolerance increased iteration counts in these experiments. Larger graphs increased execution time substantially.
