import numpy as np
from functools import reduce


class DualSimplex:
    def __init__(self, A, b, c, d_lo, d_hi):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.d_lo = np.array(d_lo)
        self.d_hi = np.array(d_hi)

        self.n, self.m = self.A.shape
    
    def solve(self, J):
        A_b = self.A[:, J]
        c_b = self.c[J]

        B = np.linalg.inv(A_b)

        y = np.dot(c_b, B)
        delta = np.dot(y, self.A) - self.c
        
        J_n = [i for i in range(self.m) if i not in J]
        J_nn = [j for j in J_n if delta[j] < 0]
        J_np = [j for j in J_n if delta[j] >= 0]
        
        return self.__solve(J, J_n, J_nn, J_np, delta, B)
    
    def __build_N(self, J, B, J_n, J_np):
        N = np.zeros(self.m)
        N[J_n] = [self.d_lo[j] if j in J_np else self.d_hi[j] for j in J_n]

        AjNj = reduce(lambda a, b: a + b, [self.A[:, j] * N[j] for j in J_n])
        print('sum of Aj*NjAjNj:', AjNj)
        N[J] = np.dot(B, self.b - AjNj)

        return N

    def __is_optimal(self, N, J):
        optimal = True
        jk = 0
        for i, n in enumerate(N):
            if i not in J: continue
            if not self.d_lo[i] <= N[i] <= self.d_hi[i]:
                optimal = False
                jk = i
                break
        
        return optimal, jk

    def __solve(self, J, J_n, J_nn, J_np, delta, B):
        print('J_nn:', J_nn)
        print('J_np:', J_np)

        N = self.__build_N(J, B, J_n, J_np)
        print('N:', N)
        
        optimal, jk = self.__is_optimal(N, J)
        
        if optimal:
            return J, y, np.dot(c, y)
        
        k = J.index(jk)

        mu_jk = 1 if N[jk] < self.d_lo[jk] else -1 # 1 если меньше минимального, -1 если больше максимального
        
        dy = mu_jk * B[k]

        mu = np.dot(dy, self.A)
        mu[jk] = mu_jk
        
        sigma = {}
        for j in J_n:
            if j in J_np and mu[j] < 0 or j in J_nn and mu[j] > 0:
                sigma[j] = -delta[j] / mu[j]
            else:
                sigma[j] = np.inf
        
        sigma0 = np.inf
        js = 0
        for k, v in sigma.items():
            if v < sigma0:
                sigma0 = v
                js = k
        
        if sigma0 == np.inf:
            raise Exception("sdf")

        delta_new = delta + sigma0 * mu
        
        J[J.index(jk)] = js 
        B = np.linalg.inv(self.A[:, J])
        
        if mu[jk] == 1 and js in J_np:
            J_np[J_np.index(js)] = jk
        elif mu[jk] == -1 and js in J_np:
            J_np.remove(js)
        elif mu[jk] == 1 and js not in J_np:
            J_np.append(jk)
        elif mu[jk] == -1 and js not in J_np:
            pass
        
        J_n = [i for i in range(self.m) if i not in J]
        J_nn = [j for j in J_n if j not in J_np]
        print(J_np, J_nn)

        self.__solve(J, J_n, J_nn, J_np, delta, B)