import numpy as np

from dual_task import DualTask
from dual import DualSimplex



class BranchAndBound:
    def __init__(self, initial_task):
        self.initial_task = initial_task

        self.iteration = 0
        self.queue = [initial_task]
        self.mu = 0
        self.x = None

    def solve(self):
        if self.iteration == 10000:
            raise Exception("Достигнут лимит итераций")
