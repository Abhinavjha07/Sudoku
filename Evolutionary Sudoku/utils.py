import numpy as np
import random
from Candidate import Candidate

random.seed(100)
dim = 9


class Given(Candidate):

    def __init__(self, values):
        self.values = values
        return

    def is_row_duplicate(self, row, v):
        for col in range(dim):
            if self.values[row][col] == v:
                return True
        return False

    def is_column_duplicate(self, col, v):
        for row in range(dim):
            if self.values[row][col] == v:
                return True

        return False

    def is_block_duplicate(self, row, col, v):
        i = 3 * (int(row / 3))
        j = 3 * (int(col / 3))

        for k in range(i, i + 3):
            for l in range(j, j + 3):
                if self.values[k][l] == v:
                    return True

        return False


class Tournament(object):
    def __init__(self):
        return

    def compete(self, candidates):
        cand1 = candidates[random.randint(0, len(candidates) - 1)]
        cand2 = candidates[random.randint(0, len(candidates) - 1)]
        fit1 = cand1.fitness
        fit2 = cand2.fitness

        if fit1 > fit2:
            fittest = cand1
            weakest = cand2

        else:
            fittest = cand2
            weakest = cand1

        selection_rate = 0.8
        r = random.uniform(0, 1)
        if r < selection_rate:
            return fittest
        else:
            return weakest
