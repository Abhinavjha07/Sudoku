import numpy as np
import random
from Candidate import Candidate

random.seed(100)
dim = 9


class CycleCrossover(object):
    def __init__(self):
        return

    def crossover(self, parent1, parent2, given, crossover_rate=1.0):
        child1 = Candidate()
        child2 = Candidate()

        child1.values = np.copy(parent1.values)
        child2.values = np.copy(parent2.values)

        r = random.uniform(0, 1)

        if r < crossover_rate:
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(0, 8)

            while crossover_point1 == crossover_point2:
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(0, 8)

            crossover_point1, crossover_point2 = min(crossover_point1, crossover_point2), max(crossover_point1,
                                                                                              crossover_point2)

            for i in range(crossover_point1, crossover_point2):
                child1.values[i], child2.values[i] = self.crossover_rows(child1.values[i], child2.values[i], i, given)

        return child1, child2

    def crossover_rows(self, row1, row2, indx, given):

        child_row1 = np.zeros(dim)
        child_row2 = np.zeros(dim)

        remaining = list(range(1, dim + 1))

        cycle = 0

        while (0 in child_row1) and (0 in child_row2):
            if cycle % 2 == 0:
                index = self.find_unused(row1, remaining)
                if given.values[indx][index] != 0:
                    child_row1[index] = given.values[indx][index]
                    child_row2[index] = given.values[indx][index]
                    remaining.remove(given.values[indx][index])
                    cycle += 1
                    continue

                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row1[index]
                child_row2[index] = row2[index]

                next = row2[index]

                while next != start:

                    index = self.find_value(row1, next)

                    if given.values[indx][index] != 0:
                        child_row1[index] = given.values[indx][index]
                        child_row2[index] = given.values[indx][index]
                        remaining.remove(given.values[indx][index])
                        break

                    child_row1[index] = row1[index]

                    remaining.remove(row1[index])
                    child_row2[index] = row2[index]
                    next = row2[index]

                cycle += 1

            else:
                index = self.find_unused(row1, remaining)
                if given.values[indx][index] != 0:
                    child_row1[index] = given.values[indx][index]
                    child_row2[index] = given.values[indx][index]
                    remaining.remove(given.values[indx][index])
                    cycle += 1
                    continue
                start = row1[index]

                remaining.remove(row1[index])
                child_row1[index] = row2[index]
                child_row2[index] = row1[index]

                next = row2[index]

                while next != start:
                    index = self.find_value(row1, next)
                    if given.values[indx][index] != 0:
                        child_row1[index] = given.values[indx][index]
                        child_row2[index] = given.values[indx][index]
                        remaining.remove(given.values[indx][index])
                        break

                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]

                    next = row2[index]

                cycle += 1

        return child_row1, child_row2

    def find_unused(self, parent_row, remaining):
        for i in range(len(parent_row)):
            if int(parent_row[i]) in remaining:
                return i

    def find_value(self, parent_row, value):
        for i in range(len(parent_row)):
            if int(parent_row[i]) == value:
                return i
