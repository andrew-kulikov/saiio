import unittest
import numpy as np


def solve(G, n, s):
    d = np.full((n,), np.inf)
    used = np.full((n,), False)
    d[s] = 0

    def find_best():
        cur_d = np.inf
        cur_pos = 0
        for i in range(n):
            if not used[i] and d[i] < cur_d:
                cur_d = d[i]
                cur_pos = i
        return cur_d, cur_pos

    for i in range(n):
        cur_d, cur_pos = find_best()
        used[cur_pos] = True
        for to, w in G[cur_pos]:
            d[to] = min(d[to], cur_d + w)
    
    return d
    

def build_graph(pairs):
    n = max(map(lambda p: max(p[0], p[1]), pairs))
    G = [[] for _ in range(n)]
    for from_, to, weight in pairs:
        G[from_ - 1].append((to - 1, weight))
    return G[:n], n


class DijkstraTestCase(unittest.TestCase):
    def test_task1(self):
        pairs = [
            (1, 2, 5), (1, 8, 3), (7, 1, 2),
            (8, 2, 1), (2, 7, 3), (2, 3, 2),
            (7, 3, 2), (8, 7, 4), (8, 9, 1),
            (7, 6, 5), (6, 8, 6), (6, 9, 2),
            (6, 3, 4), (4, 3, 2), (6, 5, 1),
            (9, 10, 5), (10, 6, 3), (10, 4, 6),
            (5, 10, 2), (5, 4, 1), (3, 5, 5)
        ]
        ans = [0, 4, 6, 12, 11, 12, 7, 3, 4, 9]

        G, n = build_graph(pairs)
        res = list(solve(G, n, 0))
        self.assertListEqual(ans, res)
    
    def test_task2(self):
        pairs = [
            (1, 2, 6), (1, 3, 2), (1, 7, 2),
            (2, 3, 5), (2, 6, 6),
            (3, 6, 1),
            (4, 3, 2), (4, 5, 3),
            (5, 8, 4),
            (6, 1, 4), (6, 7, 3), (6, 8, 7), (6, 5, 6),
            (7, 8, 4),
            (8, 2, 1), (8, 9, 1),
            (9, 6, 2), (9, 4, 1), (9, 5, 5)
        ]
        ans = [0, 6, 10, 8, 11, 9, 2, 7]

        G, n = build_graph(pairs)
        res = list(solve(G, n, 0))
        self.assertListEqual(ans, res)

if __name__ == "__main__":
    unittest.main()
