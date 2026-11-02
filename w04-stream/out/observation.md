# Week 04 — Observations

## Task 1 — Sketches

The Bloom filter had no false negatives, and its measured false-positive rate was 0.820%, close to the predicted 0.860%. The FM algorithm estimated 18,505 distinct elements compared with the actual 19,953, while reservoir sampling showed an 8.9% spread.

## Task 2 — Limits

Exact counting used 46.6 MB at 1,600,000 items and completed in 5.95 seconds, while FM required 768.66 seconds. Exact counting was faster in this Python implementation, but its memory usage increased with data size. The memory limit was not reached in the tested range.

## Task 3 — Optimized Bloom Filter

Using seven hash functions instead of one reduced the false-positive rate from 9.511% to 0.820%, a 91.4% reduction, with zero false negatives and the same 80,000-bit memory budget. When the number of inserted items is unknown, I would estimate it from the stream or use a scalable Bloom filter to maintain a low false-positive rate.