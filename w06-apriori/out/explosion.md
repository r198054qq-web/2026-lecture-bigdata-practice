# Task 2 — Support Threshold Explosion

| Support | Frequent Pairs | Peak Counters | Time (s) | Peak Memory (MB) |
|---|---:|---:|---:|---:|
| 400 | 249 | 10,585 | 0.76 | 1.1 |
| 200 | 776 | 58,626 | 1.08 | 6.4 |
| 100 | 2,244 | 273,701 | 2.07 | 26.4 |
| 50 | 6,397 | 820,259 | 3.23 | 102.2 |
| 25 | 17,045 | 893,456 | 3.67 | 102.2 |
| 12 | 43,116 | 893,456 | 3.85 | 102.8 |
| 6 | 101,938 | 893,456 | 3.84 | 119.4 |

## Observations

Lowering the support threshold from 400 to 6 increased the number of frequent pairs from 249 to 101,938.

The peak number of candidate counters increased to 893,456 and then remained constant as the threshold decreased further.

Peak memory reached 119.4 MB at support 6. No memory failure occurred during these experiments.

## Conclusion

Lower support thresholds produce many more frequent pairs and increase memory requirements. The experiment did not reach the machine's memory limit, but it demonstrated the cost of storing candidate pair counters.
