import copy
import random

INF = 999999999


class Graph():

    def  __init__(self):
        self.num_vertices = 0
        self.num_edges = 0

        self.graph = {}

        self.vertices_list = []

    def get_graph(self):

        print("Enter the number of edges: ",end="")
        self.num_edges = int(input())

        print("Enter the edges in the graph in the format A B 4 (newline) B C 7:")

        for _ in range(self.num_edges):
            info = input().split()
            if info[0] not in self.graph:
                self.graph[info[0]] = {}
                self.vertices_list.append(info[0])

            self.graph[info[0]][info[1]] = int(info[2])
            
            if info[1] not in self.graph:
                self.graph[info[1]] = {}
                self.vertices_list.append(info[1])
                
            self.graph[info[1]][info[0]] = int(info[2])
        
        self.num_vertices = len(self.graph.keys())

class Genetic_Algo():
    def __init__(self, graph_obj, initial_popu_size = 25, generations_to_check = 40, gen_size = 10):
        self.graph_obj = graph_obj

        self.initial_popu_size = initial_popu_size
        self.generations_to_check = generations_to_check
        self.gen_size = gen_size

        self.population = []

    def generate_genome(self):
        genome = copy.deepcopy(self.graph_obj.vertices_list)
        random.shuffle(genome)
        return genome

    def generate_population(self):
        for _ in range(self.initial_popu_size):
            genome = self.generate_genome()
            self.population.append([self.fitness(genome), genome])

    def fitness(self, genome):
        path_length = 0
        size = self.graph_obj.num_vertices

        for i in range(size - 1):
            if genome[i+1] in self.graph_obj.graph[genome[i]]:
                path_length += self.graph_obj.graph[genome[i]][genome[i+1]]
            else:
                path_length += INF

        if genome[0] in self.graph_obj.graph[genome[size - 1]]:
            path_length += self.graph_obj.graph[genome[size - 1]][genome[0]]
        else:
            path_length += INF

        return path_length

    def select_parents(self):
        parents = random.choices([i[1] for i in self.population], weights=[1/i[0] for i in self.population], k=2)
        return parents

    def crossover(self, parent_1, parent_2):
        child_1 = copy.deepcopy(parent_1)
        child_2 = copy.deepcopy(parent_2)

        crossover_index = random.randint(1, self.graph_obj.num_vertices - 2) 

        for i in range(crossover_index):
            swap_index = -1

            for j in range(self.graph_obj.num_vertices - 1):
                if child_1[j] == parent_2[i]:
                    swap_index = j 
                    break
            
            child_1[i], child_1[swap_index] = child_1[swap_index], child_1[i]

        for i in range(crossover_index):
            swap_index = -1

            for j in range(self.graph_obj.num_vertices - 1):
                if child_2[j] == parent_1[i]:
                    swap_index = j 
                    break
            
            child_2[i], child_2[swap_index] = child_2[swap_index], child_2[i]

        return child_1, child_2

    def mutation(self, genome):
        index_1 = random.randint(0, self.graph_obj.num_vertices - 1)
        index_2 = random.randint(0, self.graph_obj.num_vertices - 1)

        genome[index_1], genome[index_2] = genome[index_2], genome[index_1]

        return genome

    def print_fittest(self):
        print("Best solution after " + str(self.generations_to_check) + " generations :")
        path = sorted(self.population, key=lambda x: x[0])[0][1]

        size = self.graph_obj.num_vertices
        total_dist = 0

        for i in range(size - 1):
            cost = 0
            if path[i+1] in self.graph_obj.graph[path[i]]:
                cost = self.graph_obj.graph[path[i]][path[i+1]]
            else:
                cost = INF

            print("CITY {} -- {} km --> CITY {}".format(path[i], cost, path[i+1]))
            total_dist += cost

        cost = 0
        if path[0] in self.graph_obj.graph[path[size - 1]]:
            cost = self.graph_obj.graph[path[size - 1]][path[0]]
        else:
            cost = INF

        print("CITY {} -- {} km --> CITY {}".format(path[size - 1], cost, path[0]))
        total_dist += cost

        print("\nTotal distance : ", total_dist)

    def genetic_search(self):
        self.generate_population()

        for i in range(self.generations_to_check):
            print("Generation -> ",i+1,"\n")

            next_gen = sorted(self.population, key=lambda x: x[0])[0:self.gen_size//4]

            print("\tBest from current gen:")
        
            print("\t\t",next_gen[0][1],"->",next_gen[0][0])
            print("\t\t",next_gen[1][1],"->",next_gen[1][0])

            children_req = (self.gen_size - self.gen_size//4) // 2

            for j in range(children_req):
                parents = self.select_parents()
                child_1, child_2 = self.crossover(parents[0],parents[1])

                child_1 = self.mutation(child_1)
                child_2 = self.mutation(child_2)

                next_gen.append([self.fitness(child_1), child_1])
                next_gen.append([self.fitness(child_2), child_2])

            print("\n")

            self.population = next_gen
        
        self.print_fittest()

graph_obj = Graph()
graph_obj.get_graph()

gen_algo_obj = Genetic_Algo(graph_obj, 50, 25, 25)
gen_algo_obj.genetic_search()