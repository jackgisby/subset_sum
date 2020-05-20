# Subset Sum
Efficient implementation of the pseudo-polynomial subset sum algorithm in Python, with options for parallelisation 
using multiprocessing. The majority of efficient subset sum solutions are focussed on verifying the presence of a 
possible sum; most implementations appear to return, at most, a single possible answer. I use a recursive function to 
obtain all possible subsets, which appears to perform better than more simple non-dynamic recursive implementations. 

This was implemented to obtain the possible sets of masses from high-throughput MS metabolomics experiments, which 
requires non-exact matching of subsets. We therefore first obtain subsets at integer mass level, then further refine 
these results using a non-exact version of subset sum. This also means that the variable usually named "sum" has been
referred to as "mass" here, instead.

Note that, since we return all possible subsets, the backtracking portion of the dp algorithm has exponential 
complexity; this solution will still struggle for large inputs. I'm not aware of any methods to avoid this when we
wish to return all possible subsets.


## Refs
- Naive and dynamic subset sum implementation in Python. Returns True/False, does not produce the actual subset. https://github.com/KatzMitch/SubsetSum/blob/master/subsetsum.py
- Dynamic subset sum problem implementation in c++ that prints all subsets. https://www.geeksforgeeks.org/perfect-sum-problem-print-subsets-given-sum/
- Metaboverse
