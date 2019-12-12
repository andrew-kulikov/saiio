import numpy as np
from ford import ford
from pprint import pprint


MAX_VALUE = float("inf")


def build_reversed_adjacency_list(graph, debug=True):
    adj_list = {}
    for v, sub_v in graph.items():
        for k, x in sub_v.items():
            adj_list[k] = adj_list.get(k, []) + [v]
    if debug:
        print("Reversed adjacency list:\n {}".format(adj_list))
    return adj_list


def first_costs_transform(costs):
    n, m = costs.shape
    for i in range(n):
        costs[i, :] -= np.min(costs[i, :])
    for i in range(m):
        costs[:, i] -= np.min(costs[:, i])

    return costs


def build_pairs(costs: np.ndarray):
    n, m = costs.shape
    graph = []
    for i in range(n):
        for j in range(m):
            if costs[i][j] == 0:
                graph.append((i + 1, j + n + 1, 1))
    for i in range(n, 2 * n):
        graph.append((i + 1, 2 * n + 1, 1))
    for i in range(n):
        graph.append((0, i + 1, 1))

    return graph


def step2(flow, costs, L):
    n, m = costs.shape

    N1 = np.array([i for i in range(n) if i + 1 in L], dtype=np.int)
    N2 = [i for i in range(n) if i + n + 1 in L]
    N2_inv = np.array(list(set(range(n)) - set(N2)), dtype=np.int)

    с = costs[N1, :]
    с = с[:, N2_inv]
    alpha = np.min(с)

    for i in range(n):
        for j in range(m):
            if i in N1 and j not in N2:
                costs[i, j] -= alpha
            if i not in N1 and j in N2:
                costs[j, i] += alpha

    return costs


def prepare_answer(flow, costs, n):
    ans = []
    total_cost = 0

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if flow.get(i, {}).get(j + n, 0) != 1: continue
            
            ans.append(j - 1)
            total_cost += costs[i - 1, j - 1]

    return ans, total_cost


def assignment_solve(costs):
    src_costs = costs.copy()
    n, _ = costs.shape

    costs = first_costs_transform(costs)

    print('Costs matrix after first transform')
    print(costs)

    while True:
        graph = build_pairs(np.array(costs))
        max_flow, current_flow, L = ford(graph, 0, 2*n+1)

        print('Max flow: ', max_flow)
        pprint(current_flow)
        
        if max_flow == n:
            return prepare_answer(current_flow, src_costs, n)
        costs = step2(current_flow, costs, L)            


def get_test_data():
    costs = np.array([
        [2, -1, 9, 4],
        [3, 2, 5, 1],
        [13, 0, -3, 4],
        [5, 6, 1, 2]
    ])

    return costs


def main():
    costs = get_test_data()
    ans, costs = assignment_solve(costs)
    print("Ans: ", ans)
    print("Costs: ", costs)


if __name__ == '__main__':
    main()
