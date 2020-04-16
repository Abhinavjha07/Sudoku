import numpy as np
import random
from Candidate import Candidate

random.seed(100)
dim = 9

class Population(object):

    def __init__(self):
        self.candidates = []
        return

    def seed(self,nc,given):
        self.candidates = []
        
        helper = Candidate()
        helper.values = [[[] for j in range(dim)] for i in range(dim)]

        for row in range(dim):
            for col in range(dim):
                for v in range(1,10):
                    if ( given.values[row][col] == 0 and not (given.is_column_duplicate(col,v) or given.is_block_duplicate(row,col,v) or given.is_row_duplicate(row,v))):
                        helper.values[row][col].append(v)

                    elif ( given.values[row][col] != 0 ):
                        helper.values[row][col].append(given.values[row][col])
                        break


        for p in range(nc):
            X = Candidate()

            for i in range(dim):
                row = np.zeros(dim)
                for j in range(dim):

                    if given.values[i][j] != 0:
                        row[j] = int(given.values[i][j])

                    elif given.values[i][j] == 0:
                        row[j] = int(helper.values[i][j][random.randint(0,len(helper.values[i][j])-1)])

                while(len(set(row)) != dim):
                    for j in range(dim):
                        if given.values[i][j] == 0:
                            row[j] = int(helper.values[i][j][random.randint(0,len(helper.values[i][j])-1)])

                X.values[i] = row
            X.values =  np.int_(X.values)
            self.candidates.append(X)

        self.update_fitness()

        return

    def update_fitness(self):
        for candidate in self.candidates:
            candidate.update_fitness()
        return

    def sort(self):
        self.candidates.sort(key = lambda x: x.fitness,reverse = True)
        return
