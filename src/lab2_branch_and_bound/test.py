import unittest
from bnb import BranchAndBound


class BranchAndBoundTestCase(unittest.TestCase):
    def test_task1(self):
        A = [[1, 0, 0, 12, 1, -3, 4, -1],
             [0, 1, 0, 11, 12, 3, 5, 3],
             [0, 0, 1, 1, 0, 22, -2, 1]]
        b = [40, 107, 61]
        c = [2, 1, -2, -1, 4, -5, 5, 5]
        d_lo = [0, 0, 0, 0, 0, 0, 0, 0]
        d_hi = [3, 5, 5, 3, 4, 5, 6, 3]

        dual = BranchAndBound(A, b, c, d_lo, d_hi)
        x, J, f_val = dual.solve([3, 4, 5])

        x_expected = [1, 1, 2, 2, 3, 3, 6, 3]
        for i, xi in enumerate(x):
            self.assertAlmostEqual(xi, x_expected[i], 4)
        self.assertAlmostEqual(f_val, 39, 5)


if __name__ == "__main__":
    unittest.main()
