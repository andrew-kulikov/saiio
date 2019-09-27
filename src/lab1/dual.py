import numpy as np


class DualSimplex:
    def __init__(self, A, b, c, d_lo, d_hi):
        self.A = A
        self.b = b
        self.c = c
        self.d_lo = d_lo
        self.d_hi = d_hi
    
    def solve(self):
        pass
