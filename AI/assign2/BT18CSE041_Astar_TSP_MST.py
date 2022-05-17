import copy

INF = 99999999999


class Graph():

    def  __init__(self):
        self.num_vertices = 0
        self.num_edges = 0
        self.graph = {}

    def get_graph(self):

        print("Enter the number of edges: ",end="")
        self.num_edges = int(input())

        print("Enter the edges in the graph in the format A B 4 (newline) B C 7:")

        for _ in range(self.num_edges):
            info = input().split()
            if info[0] not in self.graph:
                self.graph[info[0]] = {}

            self.graph[info[0]][info[1]] = int(info[2])
            
            if info[1] not in self.graph:
                self.graph[info[1]] = {}
                
            self.graph[info[1]][info[0]] = int(info[2])
        
        self.num_vertices = len(self.graph.keys())

    def get_MST(self, start_vertex, unavailable):

        distances = {}
        in_MST = {}
        parent_ver = {}
        vertices_in_MST = 0

        no_MST = False

        num_available_vertices = self.num_vertices - len(unavailable)

        sum_edges_in_MST = 0

        for i in self.graph.keys():
            distances[i] = INF
            in_MST[i] = False
            parent_ver[i] = ""

        distances[start_vertex] = 0
        ver = start_vertex
        in_MST[ver] = True
        vertices_in_MST += 1

        for i in self.graph[ver]:
            if i not in unavailable and distances[ver] + self.graph[ver][i] < distances[i]:
                distances[i] = distances[ver] + self.graph[ver][i]
                parent_ver[i] = ver

        while vertices_in_MST < num_available_vertices:
            min = INF

            for i in distances:
                if i not in unavailable and not in_MST[i] and distances[i] < min:
                    min = distances[i]
                    ver = i 
            
            if min == INF:
                sum_edges_in_MST = -1
                no_MST = True
                break

            else:
                in_MST[ver] = True
                vertices_in_MST += 1

                for i in self.graph[ver]:
                    if i not in unavailable and distances[ver] + self.graph[ver][i] < distances[i]:
                        distances[i] = distances[ver] + self.graph[ver][i]
                        parent_ver[i] = ver

        # print(unavailable)
        # print(parent_ver)

        if not no_MST:
            for i in parent_ver:
                if i not in unavailable and i != start_vertex:
                    if parent_ver[i] != "":
                        sum_edges_in_MST += self.graph[parent_ver[i]][i]
                    else:
                        sum_edges_in_MST = -1
                        break
                    
        else:
            sum_edges_in_MST = -1

        return sum_edges_in_MST

class Astar_search_TSP():

    def __init__(self, start_city, graph_obj):
        self.start_city = start_city
        self.cities = graph_obj

        self.visited = {}

        self.traversed_nodes = []

        for i in self.cities.graph.keys():
            self.visited[i] = False

        self.fringe_list = {}
        self.expanded_list = {}

        self.curr_city = ""
        self.curr_city_path = ""

        self.path = []

    def is_goal_state(self):
        retval = 1

        for i in self.visited:
            self.visited[i] = False

        parent = self.curr_city + "-" + self.curr_city_path
        
        while parent != "0":
            self.visited[parent.split('-')[0]] = True
            parent = self.expanded_list[parent][2]
            # print(parent)

        for i in self.visited:
            if not self.visited[i]:
                retval = 0
                break

        if retval == 0:
            if self.fringe_list == {}:
                retval = -1
        elif retval == 1:        
            if self.start_city not in self.cities.graph[self.curr_city]:
                if self.fringe_list == {}:
                    retval = -1
                else:
                    retval = 0

        return retval

    def print_path(self):
        total_dist = 0

        parent = self.curr_city + "-" + self.curr_city_path

        while parent != "0":
            self.path.append(parent.split('-')[0])
            parent = self.expanded_list[parent][2]

        self.path = self.path[::-1]

        size = self.cities.num_vertices

        print()
        for i in range(size - 1):
            print("CITY {} -- {} km --> CITY {}".format(self.path[i], self.cities.graph[self.path[i]][self.path[i+1]], self.path[i+1]))
            total_dist += self.cities.graph[self.path[i]][self.path[i+1]]

        print("CITY {} -- {} km --> CITY {}".format(self.path[size - 1], self.cities.graph[self.path[size - 1]][self.path[0]], self.path[0]))
        total_dist += self.cities.graph[self.path[size - 1]][self.path[0]]

        print("\nTotal distance : ", total_dist)

    def change_curr_city(self):
        min_city = ""
        min_f_of_city = INF

        for i in self.fringe_list:
            if self.fringe_list[i][1] < min_f_of_city:
                min_f_of_city = self.fringe_list[i][1]
                min_city = i 

        self.curr_city = min_city.split('-')[0]
        self.curr_city_path = self.fringe_list[min_city][2]

    def search(self):
        self.curr_city = self.start_city
        self.curr_city_path = "0"

        self.fringe_list[self.curr_city + "-" + self.curr_city_path] = [0, self.cities.get_MST(self.curr_city, []), "0"]

        while True:

            unavailable = [self.curr_city]
            parent = self.fringe_list[self.curr_city + "-" + self.curr_city_path][2]

            while parent != "0":
                unavailable.append(parent.split('-')[0])
                parent = self.expanded_list[parent][2]

            # print(self.curr_city)
            # print(unavailable)
            
            for i in self.cities.graph[self.curr_city]:
                if i not in unavailable:

                    g_of_city = self.cities.graph[self.curr_city][i] + self.fringe_list[self.curr_city + "-" + self.curr_city_path][0]
                    heuristic = self.cities.get_MST(i, unavailable)

                    if heuristic != -1:
                        self.fringe_list[i + "-" + self.curr_city + "-" + self.curr_city_path] = [g_of_city, g_of_city + heuristic, self.curr_city + "-" + self.curr_city_path]
            
            self.traversed_nodes.append(self.curr_city + "-" + self.curr_city_path)
            self.expanded_list[self.curr_city + "-" + self.curr_city_path] = copy.deepcopy(self.fringe_list[self.curr_city + "-" + self.curr_city_path])
            del self.fringe_list[self.curr_city + "-" + self.curr_city_path]

            # print(self.fringe_list)
            # print(self.expanded_list)
            
            solution = self.is_goal_state()
            
            if solution == 1:
                self.print_path()
                break
            elif solution == -1:
                print("No solution exists for the given graph of cities!")
                break
            else:
                self.change_curr_city()


graph_obj = Graph()
graph_obj.get_graph()

start_node = input("Enter start node: ")

TSP = Astar_search_TSP(start_node, graph_obj)
TSP.search()
