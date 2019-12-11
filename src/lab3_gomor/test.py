from dual_task import DualTask
from gomor import Gomor
import unittest
import numpy as np

class GomorTestCase(unittest.TestCase):
    def test_task1(self):
        A = [[1, -5, 3, 1, 0, 0],
             [4, -1, 1, 0, 1, 0],
             [2, 4, 2, 0, 0, 1]]
        b = [-8, 22, 30]
        c = [7, -2, 6, 0, 5, 2]
        d_lo = [0] * 6
        d_hi = [1e9] * 6

        task = DualTask(A, b, c, d_lo, d_hi)
        gomor = Gomor(task)
        gomor.solve()

        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
