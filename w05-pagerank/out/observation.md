# Week 05 — PageRank Observations

## Task 1 — PageRank and Its Failure Cases

Without teleportation, a dead end causes rank to disappear from the graph, and the total rank eventually becomes zero. A spider trap absorbs all rank because its nodes only link to each other. With beta = 0.85, teleportation and dead-end redistribution preserve the total rank of 1 and prevent spider traps from absorbing everything.

## Task 2 — PageRank Convergence

Increasing beta from 0.5 to 0.99 increased the required iterations from 14 to 24. For the 20,000-node graph, beta = 0.85 required 21 iterations (0.306 seconds), while beta = 0.95 required 24 iterations (0.414 seconds). Tightening the tolerance from 1e-6 to 1e-12 increased the iterations from 12 to 25.

## Task 3 — Sparse PageRank

The sparse implementation processes only existing edges instead of storing a dense transition matrix. For 1,200 nodes and 5,877 edges, it was 55.9 times faster and used 600 times fewer floats. The maximum rank difference was 1.18e-15, satisfying the required accuracy of 1e-9.

### R5 — Why Teleportation Does Not Require a Dense Matrix

Teleportation adds the same value, (1 - beta) / n, to every node, so it can be computed directly without constructing a dense matrix. The total rank of dead-end nodes is collected into one scalar and redistributed uniformly. Therefore, the sparse implementation only processes existing edges while preserving the same PageRank results as the dense implementation.