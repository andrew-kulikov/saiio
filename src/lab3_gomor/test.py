from dual_task import DualTask
import unittest


class GomorTestCase(unittest.TestCase):
    def test_task1(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
