from .dual_task import DualTask
from .dual import DualSimplex

def select_first_not_in(J, n):
    for i in range(n):
        if i not in J:
            return i


def is_int(x):
    return abs(round(x) - x) < 0.001


def all_int(a):
    return all(is_int(x) for x in a)


class Gomor:
    def __init__(self, task: DualTask):
        self.task = task
        self.cur_task: DualTask = task

        self.J_art = []
        self.art_limitations = {}

    def exclude_artificial(self, x: list, J: list):
        for col in J:
            if col in self.J_art:
                row = self.art_limitations[col]
                self.cur_task.remove()



    def solve(self):
        dual = DualSimplex(self.task)
        x, J, f = dual.solve()

        print(x, J, f)
        
        if all_int(x):
            return x, J, f

        jk = select_first_not_in(J, self.cur_task.n)
        print(jk)



