# Task 2 - Crossover Measurement

## Timing Results

| n | Brute Force (s) | LSH (s) |
|---:|---:|---:|
| 100 | 0.03 | 1.10 |
| 250 | 0.17 | 2.68 |
| 500 | 0.66 | 5.26 |
| 1000 | 2.65 | 10.75 |
| 2000 | 11.04 | 20.83 |

## A3 - Time versus n

Brute force becomes much slower as n increases because it compares every pair.
LSH grows more gradually, but on the available dataset its hashing overhead makes
it slower than brute force for the measured sizes.

## A4 - Quadratic Check

The brute-force measurements approximately follow quadratic growth.
From n=500 to n=1000, the time increased from 0.66 s to 2.65 s, about 4.02 times.
From n=1000 to n=2000, it increased from 2.65 s to 11.04 s, about 4.17 times.
Therefore, doubling n roughly quadrupled the brute-force running time.

## A5 - Peak Memory

Peak memory measurements are recorded in crossover.json.
The largest valid measured document count used for the timing comparison was
n=2000.

## A6 - Machine

The machine information, including the platform, processor, and Python version,
is recorded automatically in crossover.json. Other normal desktop applications
were running during the experiment.

## A7 - Crossover

No crossover was observed within the available dataset. At n=2000, brute force
took 11.04 s while LSH took 20.83 s. The benchmark contains only 2,120 documents,
so requesting larger values does not actually provide enough documents to test
a true larger-n crossover.

## A8 - Why LSH Loses at Small n

LSH has additional setup work before exact comparisons begin. It must compute
120 MinHash values for every document, divide the signatures into bands, build
hash buckets, and generate candidate pairs. At small n, brute force does not
perform enough pairwise comparisons for this setup cost to pay off. As n grows,
brute-force comparisons grow quadratically while the signature-building work
grows approximately linearly.