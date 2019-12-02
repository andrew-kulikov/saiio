import numpy as np
import math

from dual_task import DualTask
from dual import DualSimplex

import random


def is_int(x):
    return abs(int(x) - x) < 0.001


def all_int(a):
    return all(is_int(x) for x in a)


def get_not_int(a):
    not_ints = []
    for i, x in enumerate(a):
        if not is_int(x):
            not_ints.append((i, x))

    return random.choice(not_ints)


class BranchAndBound:
    def __init__(self, initial_task):
        self.initial_task = initial_task

        self.iteration = 0
        self.queue = [initial_task]
        self.mu = 0
        self.x = None

    def __split_task(self, task, x):
        pos, x_val = get_not_int(x)
        split_val = math.floor(x_val)

        task1 = DualTask(task.A, task.b, task.c, task.d_lo, task.d_hi)
        task1.d_hi[pos] = split_val

        task2 = DualTask(task.A, task.b, task.c, task.d_lo, task.d_hi)
        task2.d_lo[pos] = split_val + 1

        return task1, task2

    def solve(self):
        if self.iteration == 10000:
            raise Exception("Достигнут лимит итераций")
        
        if len(self.queue) == 0:
            return

        task = self.queue.pop(0)
        dual = DualSimplex(task)
        x, _, f_val = dual.solve()

        if all_int(x):
            self.mu = f_val
            self.x = x
            return
        
        task1, task2 = self.__split_task(task, x)
        print(task.d_lo)
        print(task.d_hi)

        print(task1.d_lo)
        print(task1.d_hi)

        print(task2.d_lo)
        print(task2.d_hi)



