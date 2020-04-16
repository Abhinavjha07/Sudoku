import numpy as np
import random
from Population import Population
from utils import *
from CycleCrossover import CycleCrossover
random.seed(100)
dim = 9


class Sudoku(object):
    def __init__(self):
        self.given = None
        return

    def load(self,path):
        
        with open(path,'r') as f:
            values = np.loadtxt(f).reshape((dim,dim)).astype(int)
            print(values)
            self.given = Given(values)

        return

    def solve(self):
        
        nc = 100
        ne = int(0.01 * nc)
        ng = 1000
        nm = 0
        self.population = Population()
        self.population.seed(nc,self.given)
        mutation_rate = 0.2
        stale = 0
        m1 = 0
        m2 = 0
        n_calls = 0
        for generation in range(ng):
            
            print('Generation ', generation)
            best_fitness = 0.0

            for c in range(nc):
                fitness = self.population.candidates[c].fitness
                if fitness == 1:
                    print('Solution found at generation ', generation)
                    print('Initial Sudoku : ')
                    print(self.given.values)
                    print('\nSolution : ')
                    print(self.population.candidates[c].values)
                    # print(n_calls,  m1,m2)
                    return self.population.candidates[c]

                if fitness > best_fitness:
                    
                    best_fitness = fitness
            
            print('Best fitness : ',best_fitness)

            next_population = []

            self.population.sort()

            elites = []

            for e in range(ne):
                elite = Candidate()
                elite.values = np.copy(self.population.candidates[e].values)
                elites.append(elite)


            for c in range(ne,nc,2):
                t = Tournament()
                parent1 = t.compete(self.population.candidates)
                parent2 = t.compete(self.population.candidates)
                
                cross = CycleCrossover()
                
                child1,child2 = cross.crossover(parent1,parent2,self.given,crossover_rate = 1.0)
                old_fitness = child1.fitness
                n_calls += 1
                success = child1.mutate(mutation_rate,self.given)
                if success:
                    m1 += 1
                child1.update_fitness()
                
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate,self.given)
                if success :
                    m2 += 1
                child2.update_fitness()
                next_population.append(child1)
                next_population.append(child2)
                n_calls += 1

            for e in range(ne):
                next_population.append(elites[e])


            self.population.candidates = next_population
            self.population.update_fitness()

            self.population.sort()

            if(self.population.candidates[0].fitness != self.population.candidates[1].fitness):
                stale = 0

            else:
                stale += 1

            if stale >= 100:
                for c in range(nc):
                    fitness = self.population.candidates[c].fitness
                    if fitness == best_fitness:
                        print('No Solution found, best fit solution :')
                        print(self.population.candidates[c].values)
                        return self.population.candidates[c]
                


        print('No solution found')
        return None


s = Sudoku()
s.load('sudoku1.txt')
solution = s.solve()


if solution:
    with open('solution1.txt' ,'w') as f:
        np.savetxt(f,solution.values.reshape(dim*dim),fmt='%d',newline = ' ')
                





        
        
    
    



    

                        
