import itertools
import random
import sys
from pprint import pprint


def held_karp(dists):
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)
    print(C)
    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        print('='*20)
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            print(subset, bits)
            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)
                print('prev:', prev)
                res = []
                for m in subset:
                    if m == k: continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                print('k: {}, res: {}'.format(k, res))
                C[(bits, k)] = min(res)
                pprint(C)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)
    
    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        print('parent:', parent)
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))


def generate_distances(n):
    dists = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dists[i][j] = dists[j][i] = random.randint(1, 99)

    return dists


def read_distances(filename):
    dists = []
    with open(filename, 'r') as f:
        for line in f:
            # Skip comments
            if line[0] == '#':
                continue

            dists.append(list(map(int, map(str.strip, line.split(',')))))

    return dists


if __name__ == '__main__':
    dists = read_distances('ex.csv')
    #dists = generate_distances(int(arg))

    # Pretty-print the distance matrix
    for row in dists:
        print(''.join([str(n).rjust(3, ' ') for n in row]))

    print('')

    print(held_karp(dists))