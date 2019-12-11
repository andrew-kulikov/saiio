import numpy as np


class DualTask:
    def __init__(self, A: list, b: list, c: list, d_lo: list, d_hi: list):
        self.A: np.array = np.array(A)
        self.b: list = b
        self.c: list = c
        self.d_lo: np.array = np.array(d_lo)
        self.d_hi: np.array = np.array(d_hi)
        self.n, self.m = self.A.shape
    
    def remove(self, row, col):
        self.A = np.delete(self.A, row, axis=0)
        self.A = np.delete(self.A, col, axis=1)

        del self.b[row]
        del self.c[col]

        self.d_lo = np.delete(self.d_lo, col)
        self.d_hi = np.delete(self.d_hi, col)

        self.n -= 1
        self.m -= 1
