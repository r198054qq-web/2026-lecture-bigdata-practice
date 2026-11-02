# Week 07 — Observations

## Task 1 — K-means Initialization

I kept the previous centroid when a cluster became empty. Moving it to the farthest point could produce a different clustering. K-means++ achieved an average SSE of 0.120, compared with 38.513 for random initialization over 40 seeds. K-means++ requires extra initial distance calculations but usually produces better clusters. SSE alone cannot determine the best k because it decreases as k increases.

## Task 2 — Curse of Dimensionality

As dimensionality increased from 2 to 1000, the contrast ratio decreased from 488.582 to 0.153. The relative standard deviation also decreased from 0.476 to 0.019. Distance concentration became noticeable around 50–100 dimensions, making nearest-neighbor comparisons less informative.

## Task 3 — Fewer Distance Computations

My optimized K-means reduced distance computations from 10,320,000 to 6,958,182, a 32.6% reduction. Runtime decreased from 28.27 to 18.47 seconds, while the final SSE remained exactly the same at 10,737,882.94. The triangle inequality helped skip unnecessary distance calculations without changing the clustering result.