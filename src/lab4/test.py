import unittest
import numpy as np


def restore_path(B, X, c):
    path = []
    for i in range(len(B) - 1, -1, -1):
        path.append(X[i, c])
        c -= X[i, c]
    path.reverse()
    return path


def solve(F, c):
    n, m = np.shape(F)
    B = np.zeros((n, m), dtype=np.int32)
    X = np.zeros((n, m), dtype=np.int32)
    B[0] = F[0]
    X[0] = list(range(m))
    for x in range(1, n):
        for y in range(m):
            best_b = 0
            best_pos = 0
            for z in range(y + 1):
                b = F[x][z] + B[x - 1][y - z]
                if b > best_b:
                    best_b = b
                    best_pos = z
            B[x][y] = best_b
            X[x][y] = best_pos
   
    path = restore_path(B, X, c)
    
    return path, B


class OptimalTests(unittest.TestCase):
    def test_task1(self):
        F = [[0, 3, 4, 5, 8, 9, 10],
             [0, 2, 3, 7, 9, 12, 13],
             [0, 1, 2, 6, 11, 11, 13]]
        c = 6
        ans = [1, 1, 4]

        path, B = solve(F, c)
        self.assertListEqual(path, ans)
    
    def test_task2(self):
        F = [[0, 1, 2, 2, 4, 5, 6],
             [0, 2, 3, 5, 7, 7, 8],
             [0, 2, 4, 5, 6, 7, 7]]
        c = 6
        ans = [0, 4, 2]

        path, B = solve(F, c)
        self.assertListEqual(path, ans)
    
    def test_task3(self):
        F = [[0, 1, 1, 3, 6, 10, 11],
             [0, 2, 3, 5, 6, 7, 13],
             [0, 1, 4, 4, 7, 8, 9]]
        c = 6
        ans = [0, 6, 0]

        path, B = solve(F, c)
        self.assertListEqual(path, ans)

    def test_task4(self):
        F = [[0, 1, 2, 4, 8, 9, 9, 23],
             [0, 2, 4, 6, 6, 8, 10, 11],
             [0, 3, 4, 7, 7, 8, 8, 24]]
        c = 7
        ans = [0, 0, 7]

        path, B = solve(F, c)
        self.assertListEqual(path, ans)
    
    def test_task5(self):
        F = [[0, 3, 3, 6, 7, 8, 9, 14],
             [0, 2, 4, 4, 5, 6, 8, 13],
             [0, 1, 1, 2, 3, 3, 10, 11]]
        c = 7
        ans = [7, 0, 0]

        path, B = solve(F, c)
        self.assertListEqual(path, ans)

    def test_task6(self):
        F = [[0, 2, 2, 3, 5, 8, 8, 10, 17],
             [0, 1, 2, 5, 8, 10, 11, 13, 15],
             [0, 4, 4, 5, 6, 7, 13, 14, 14],
             [0, 1, 3, 6, 9, 10, 11, 14, 16]]
        c = 8
        ans = [0, 4, 1, 3]

        path, B = solve(F, c)
        self.assertListEqual(path, ans)


if __name__ == "__main__":
    unittest.main()
