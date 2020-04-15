import numpy as np
import random
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


class Candidate(object):

    def __init__(self):
        self.values = np.zeros((dim,dim))
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
            for k in range(0,dim):
                if c_count[k] == 1:
                    x += 1

            c_sum += (1.0/len(set(c_count)))/dim
                
            c_count = np.zeros(dim)

        for i in range(0,dim,3):
            for j in range(0,dim,3):
                for k in range(i,i+3):
                    for l in range(j,j+3):

                        b_count[int(self.values[k][l] - 1)] += 1
                x = 0
                for k in range(0,dim):
                    if b_count[k] == 1:
                        x += 1

                
                b_sum += (1.0/len(set(b_count)))/dim
                b_count = np.zeros(dim)


        if int(c_sum) == 1 and int(b_sum) == 1:
            fitness = 1.0

        else:
            fitness = c_sum * b_sum

        self.fitness = fitness

        return

    
    #need to complete this one
    def mutate(self,mutation_rate,given):
        r = random.uniform(0,1)
        success = False
        if r < mutation_rate:
            while(not success):
                row1 = random.randint(0,8)
                row2 = row1

                
                from_col = random.randint(0,8)
                to_col = random.randint(0,8)

                while(from_col == to_col):
                    from_col = random.randint(0,8)
                    to_col = random.randint(0,8)


                if(given.values[row1][from_col] == 0 and given.values[row1][to_col] == 0):
                    if(not given.is_column_duplicate(to_col, self.values[row1][from_col])
                       and not given.is_column_duplicate(from_col, self.values[row2][to_col])
                        and not given.is_block_duplicate(row2, to_col, self.values[row1][from_col])
                       and not given.is_block_duplicate(row1, from_col, self.values[row2][to_col])):
                        temp = self.values[row2][to_col]
                        self.values[row2][to_col] = self.values[row1][from_col]
                        self.values[row1][from_col] = temp
                        success = True
                    

        return success
        

class Given(Candidate):

    def __init__(self,values):
        self.values = values
        return

    def is_row_duplicate(self,row,v):
        for col in range(dim):
            if self.values[row][col] == v:
                return True
        return False

    def is_column_duplicate(self,col,v):
        for row in range(dim):
            if self.values[row][col] == v:
                return True

        return False

    def is_block_duplicate(self,row,col,v):
        i = 3*(int(row/3))
        j = 3*(int(col/3))

        for k in range(i,i+3):
            for l in range(j,j+3):
                if self.values[k][l] == v:
                    return True

        return False



class Tournament(object):
    def __init__(self):
        return

    def compete(self,candidates):
        cand1 = candidates[random.randint(0,len(candidates)-1)]
        cand2 = candidates[random.randint(0,len(candidates)-1)]
        fit1 = cand1.fitness
        fit2 = cand2.fitness

        if fit1>fit2:
            fittest = cand1
            weakest = cand2

        else:
            fittest = cand2
            weakest = cand1

        selection_rate = 0.8
        r = random.uniform(0,1)
        if r < selection_rate:
            return fittest
        else:
            return weakest


class CycleCrossover(object):
    def __init__(self):
        return

    def crossover(self,parent1,parent2,given,crossover_rate = 1.0):
        child1 = Candidate()
        child2 = Candidate()

        child1.values = np.copy(parent1.values)
        child2.values = np.copy(parent2.values)

        r = random.uniform(0,1)

        if r < crossover_rate:
            crossover_point1 = random.randint(0,8)
            crossover_point2 = random.randint(0,8)

            while(crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0,8)
                crossover_point2 = random.randint(0,8)

            crossover_point1, crossover_point2 = min(crossover_point1,crossover_point2), max(crossover_point1,crossover_point2)
            
            for i in range(crossover_point1,crossover_point2):
                child1.values[i],child2.values[i] = self.crossover_rows(child1.values[i],child2.values[i],i,given)

        return child1,child2


    def crossover_rows(self,row1,row2,indx,given):
        
        child_row1 = np.zeros(dim)
        child_row2 = np.zeros(dim)

        remaining = list(range(1,dim+1))
        
        cycle = 0

        while((0 in child_row1) and (0 in child_row2)):
            if(cycle % 2 == 0):
                index = self.find_unused(row1,remaining)
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
                
                while (next != start):
                    
                    index = self.find_value(row1,next)
                    
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
                index = self.find_unused(row1,remaining)
                if given.values[indx][index] != 0 :
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

                while(next != start):
                    index = self.find_value(row1, next)
                    if given.values[indx][index] != 0 :
                        child_row1[index] = given.values[indx][index]
                        child_row2[index] = given.values[indx][index]
                        remaining.remove(given.values[indx][index])
                        break
                    
                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]

                    next  = row2[index]

                cycle += 1

        return child_row1,child_row2



    def find_unused(self,parent_row,remaining):
        for i in range(len(parent_row)):
            if int(parent_row[i]) in remaining:
                return i

    def find_value(self,parent_row,value):
        for i in range(len(parent_row)):
            if int(parent_row[i]) == value:
                return i




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
                    print(n_calls,  m1,m2)
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
                





        
        
    
    



    

                        
