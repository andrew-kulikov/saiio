import unittest
from pprint import pprint
import numpy as np


DIRECTION_FORWARD = 0
DIRECTION_BACKWARD = 1


def build_graph(pairs, to):
    G = {to: {}}
    for from_, to, weight in pairs:
        if from_ not in G:
            G[from_] = {}
        G[from_][to] = weight
    return G


def build_parents_graph(pairs, s):
    G = {s: {}}
    for from_, to, weight in pairs:
        if to not in G:
            G[to] = {}
        G[to][from_] = weight
    return G


def get_start_flow(g):
    g1 = {}

    for v, connections in g.items():
        g1[v] = {}
        for to, _ in connections.items():
            g1[v][to] = 0

    return g1


def ford(pairs, s, t):
    g_forward = build_graph(pairs, t)
    g_backward = build_parents_graph(pairs, s)

    cur_flow = get_start_flow(g_forward)

    flow = 0

    while True:
        ic = 1
        it = 1
        L = [s]
        g = {s: (0, DIRECTION_FORWARD)}
        p = {s: 1}
        p_inv = {1: s}
        i = s

        while True:
            # step 2
            for j, weight in g_forward[i].items():
                if j in L or cur_flow[i][j] >= weight:
                    continue

                g[j] = (i, DIRECTION_FORWARD)
                it += 1
                p[j] = it
                p_inv[it] = j

                L.append(j)

            # step 3
            for j, weight in g_backward[i].items():
                if j in L or cur_flow[j][i] == 0:
                    continue

                g[j] = (i, DIRECTION_BACKWARD)
                it += 1
                p[j] = it
                p_inv[it] = j

                L.append(j)
            
            # step 4
            if t in L:
                break

            # step 5
            ic += 1
            if ic not in p_inv:
                break

            i = p_inv[ic]
        
        # restore flow
        if t not in g:
            return flow

        cur = t
        alpha = np.inf

        # минимальный увеличивающий поток
        while cur != s:
            prev, direction = g[cur]

            if direction == DIRECTION_FORWARD:
                allowed = g_forward[prev][cur] - cur_flow[prev][cur]
            else:
                allowed = cur_flow[cur][prev]
        
            alpha = min(alpha, allowed)
            cur = prev

        cur = t
        # обновляем путь
        while cur != s:
            prev, direction = g[cur]

            if direction == DIRECTION_FORWARD:
                cur_flow[prev][cur] += alpha
            else:
                cur_flow[cur][prev] -= alpha
            
            cur = prev
        
        flow += alpha

    return flow


class MaxFlowTestCase(unittest.TestCase):
    def test_task1(self):
        pairs = [
            [0, 1, 4], [0, 3, 9], [1, 3, 2],
            [1, 4, 4], [3, 2, 1], [3, 5, 6],
            [2, 4, 1], [2, 5, 10], [4, 5, 1],
            [4, 6, 2], [5, 6, 9]
        ]
        s = 0
        t = 6
        flow = ford(pairs, s, t)

        self.assertEqual(flow, 10)
    
    def test_task2(self):
        pairs = [
            [0, 1, 3], [0, 2, 2], [0, 3, 1], [0, 5, 6],
            [1, 3, 1], [1, 4, 2], 
            [2, 4, 2], [2, 3, 1], [2, 5, 4],
            [3, 5, 5], [3, 4, 7], [3, 6, 4], [3, 7, 1],
            [4, 6, 3], [4, 7, 2],
            [5, 7, 4],
            [6, 5, 3], [6, 7, 5]
        ]
        s = 0
        t = 7
        flow = ford(pairs, s, t)

        self.assertEqual(flow, 10)

    def test_task3(self):
        pairs = [
            [0, 1, 4], [0, 2, 1], [0, 4, 1], [0, 5, 5], [0, 6, 2],
            [1, 3, 1], [1, 5, 6], 
            [2, 4, 2],
            [3, 2, 6], [3, 6, 3],
            [4, 5, 4], [4, 7, 3],
            [5, 7, 3], [5, 6, 1], [5, 8, 6],
            [6, 7, 4], [6, 8, 5],
            [7, 8, 4]
        ]
        s = 0
        t = 8
        flow = ford(pairs, s, t)

        self.assertEqual(flow, 13)
    
    def test_task4(self):
        pairs = [
            [0, 1, 2], [0, 2, 1], [0, 4, 2],
            [1, 3, 2], [1, 4, 1], 
            [2, 4, 3], [2, 5, 2],
            [3, 6, 1], [3, 7, 2],
            [4, 5, 1], [4, 6, 4], [4, 7, 3], [4, 8, 3],
            [5, 7, 2], [5, 8, 2],
            [6, 7, 5], [6, 9, 3],
            [7, 8, 1], [7, 9, 4],
            [8, 9, 3]
        ]
        s = 0
        t = 9
        flow = ford(pairs, s, t)

        self.assertEqual(flow, 5)

    def test_task5(self):
        pairs = [
            [0, 1, 3], [0, 2, 6], [0, 3, 3], [0, 4, 2],
            [1, 2, 4], [1, 3, 1], [1, 4, 4], 
            [2, 6, 3], [2, 7, 2],
            [3, 2, 1], [3, 4, 5], [3, 6, 1], [3, 7, 2],
            [4, 5, 1],
            [5, 3, 3], [5, 6, 1],
            [6, 7, 4]
        ]
        s = 0
        t = 7
        flow = ford(pairs, s, t)

        self.assertEqual(flow, 8)


if __name__ == "__main__":
    unittest.main()
