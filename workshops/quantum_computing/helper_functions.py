import numpy as np
import networkx as nx

def naive_exact_maxcut(graph):
    """
        Gets the true optimal maximum cut naively by trying all possible cuts and taking the best one.
    """
    A = nx.adjacency_matrix(graph).toarray()
    mu = -np.ones(len(graph.nodes())) @ A
    sigma = A + np.diag(mu)

    def objective(x):
        x = np.array([float(entry) for entry in x])
        return x@sigma@x

    N = len(sigma)
    # function to generate all binary strings of length n
    saved = []
    def get_all_bitstrings(n, arr, i=0):
        if i == n:
            bitstring = ''.join(str(x) for x in arr)
            saved.append(bitstring)
            return

        # first assign "0" at ith position and try for all other permutations for remaining positions
        arr[i] = 0
        get_all_bitstrings(n, arr, i + 1)

        # and then assign "1" at ith position and try for all other permutations for remaining positions
        arr[i] = 1
        get_all_bitstrings(n, arr, i + 1)

    # get all bitstrings and initialize min and opt variables
    get_all_bitstrings(N, [None]*N)
    minimum = np.inf
    best_string = None

    # iterate through all the options, saving any improvements, then return the optimal bitstring
    for bitstring in saved:
        cut_val = objective(bitstring)
        if cut_val < minimum:
            minimum = cut_val
            best_string = bitstring
    return best_string, minimum
