# Week 03 Observations

## Task 1

I used one pass over the rows because it avoids repeatedly scanning the matrix for every column and is more suitable for data that may not fit in memory.

For leftover signature rows, I require the signature length to divide evenly by the number of bands; otherwise, the program raises a ValueError instead of silently dropping rows.

S1 and S4 had an estimated similarity of 1.0 with only two hash functions, while the true Jaccard similarity was 2/3. Using more independent hash functions would reduce the variance of the estimate, but it would require more hashing, memory, and computation.

## Task 2

On my machine, no crossover was observed within the available 2,120-document dataset. At n=2000, brute force took 11.04 s while LSH took 20.83 s.

The quadratic check held reasonably well: doubling n from 500 to 1000 increased brute-force time by about 4.02x, and doubling from 1000 to 2000 increased it by about 4.17x.

The experiment became noticeably slower around n=2000, where LSH took 20.83 s. The available benchmark data limited further genuine increases in n before memory became the limiting factor.

## Task 3

I used 120 MinHash values and 30 bands, giving 4 rows per band. The approximate S-curve step is (1/30)^(1/4) = 0.427, which is below the similarity threshold of 0.6. I chose this to favor high recall while still greatly reducing candidate comparisons.

When I initially used poorly correlated hash functions, recall was only 70.2%. After using independently generated reproducible hash parameters, recall increased to 100.0%. The final method made only 128 comparisons instead of 2,246,140, avoiding 99.99% of comparisons.

The harness treats hashing as free, but at much larger scale this becomes less realistic because generating many MinHash values for every document requires substantial CPU time and memory. At that point, signature construction and storage would become an important part of the total cost.