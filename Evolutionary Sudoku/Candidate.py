import random

import numpy as np

random.seed(100)
dim = 9


class Candidate(object):

    def __init__(self):
        self.values = np.zeros((dim, dim))
        self.fitness = None
        return

    def update_fitness(self):

        c_count = np.zeros(dim)
        b_count = np.zeros(dim)

        c_sum = 0.0
        b_sum = 0.0

        for i in range(dim):
            for j in range(dim):
                c_count[int(self.values[i][j] - 1)] += 1

            x = 0
            for k in range(0, dim):
                if c_count[k] == 1:
                    x += 1

            c_sum += (1.0 / len(set(c_count))) / dim

            c_count = np.zeros(dim)

        for i in range(0, dim, 3):
            for j in range(0, dim, 3):
                for k in range(i, i + 3):
                    for l in range(j, j + 3):
                        b_count[int(self.values[k][l] - 1)] += 1
                x = 0
                for k in range(0, dim):
                    if b_count[k] == 1:
                        x += 1

                b_sum += (1.0 / len(set(b_count))) / dim
                b_count = np.zeros(dim)

        if int(c_sum) == 1 and int(b_sum) == 1:
            fitness = 1.0

        else:
            fitness = c_sum * b_sum

        self.fitness = fitness

        return

    # need to complete this one
    def mutate(self, mutation_rate, given):
        r = random.uniform(0, 1)
        success = False
        if r < mutation_rate:
            while not success:
                row1 = random.randint(0, 8)
                row2 = row1

                from_col = random.randint(0, 8)
                to_col = random.randint(0, 8)

                while from_col == to_col:
                    from_col = random.randint(0, 8)
                    to_col = random.randint(0, 8)

                if given.values[row1][from_col] == 0 and given.values[row1][to_col] == 0:
                    if (not given.is_column_duplicate(to_col, self.values[row1][from_col])
                            and not given.is_column_duplicate(from_col, self.values[row2][to_col])
                            and not given.is_block_duplicate(row2, to_col, self.values[row1][from_col])
                            and not given.is_block_duplicate(row1, from_col, self.values[row2][to_col])):
                        temp = self.values[row2][to_col]
                        self.values[row2][to_col] = self.values[row1][from_col]
                        self.values[row1][from_col] = temp
                        success = True

        return success
