import copy

def get_hash(curr_state):
    hash_val = 0

    for i in range(3):
        for j in range(3):
            hash_val = hash_val*10 + curr_state[i][j]
    
    return hash_val

def compute_manhattan_distance(curr_state, goal_state):
    retval = 0

    for i in range(3):
        for j in range(3):
            if curr_state[i][j] != -1:
                for x in range(3):
                    found = False
                    for y in range(3):
                        if curr_state[i][j] == goal_state[x][y]:
                            retval += abs(i - x) + abs(j - y)
                            found = True
                            break
                    if found:
                        break
    
    return retval

class Bi_directional_search:

    def __init__(self):

        self.start_state = [[0,0,0], [0,0,0], [0,0,0]]
        self.goal_state = [[0,0,0], [0,0,0], [0,0,0]]

        self.curr_forw_state = []
        self.curr_backw_state = []

        self.src_path = []
        self.dest_path = []

        self.src_expanded = {}
        self.src_fringe = {}

        self.dest_expanded = {}
        self.dest_fringe = {}

        self.intersection_node_hash_val = []

        self.start_state_hash_val = -1
        self.goal_state_hash_val = -1

    def take_states(self):
        print("Print the initial state of the puzzle in 2D matrix format - space separated with 0 at the gap:")

        for i in range(3):
            self.start_state[i][0], self.start_state[i][1], self.start_state[i][2] = map(int, input().split())

        print("Print the initial state of the puzzle in 2D matrix format - space separated with 0 at the gap:")

        for i in range(3):
            self.goal_state[i][0], self.goal_state[i][1], self.goal_state[i][2] = map(int, input().split())

        self.start_state_hash_val = get_hash(self.start_state)
        self.goal_state_hash_val = get_hash(self.goal_state)

    def validate_start_state(self):
        state_str = ""
        valid = True

        for i in range(3):
            for j in range(3):
                state_str += str(self.start_state[i][j])

        # Converting state into 1-D list
        arr = [char for char in state_str]
        
        # Checking if it contains unique elements
        if len(set(arr)) != 9:
            return False

        # Counting number of inversions in the state and if it is even then returning True otherwise False.
        inversions = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != '0' and arr[i] != '0' and int(arr[i]) > int(arr[j]):
                    inversions += 1

        if inversions % 2 != 0:
            valid = False

        return valid

    def intersecting_nodes(self):
        found = False

        for forw_node_hash in self.src_expanded.keys():
            if forw_node_hash in self.dest_expanded.keys():
                self.intersection_node_hash_val = forw_node_hash 
                found = True
                break

        return found

    def expand_node_forw_search(self):
        x_index, y_index = -1, -1

        for i in range(3):
            for j in range(3):
                if self.curr_forw_state[i][j] == 0:
                    x_index = i 
                    y_index = j 
                    break

        
        parent_hash_val = get_hash(self.curr_forw_state)

        # move from up
        if x_index != 0:
            
            temp = copy.deepcopy(self.curr_forw_state)
            
            temp[x_index][y_index], temp[x_index - 1][y_index] = temp[x_index - 1][y_index],temp[x_index][y_index]
            
            hash_val = get_hash(temp)
           
            if hash_val not in self.src_expanded:
                self.src_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]
                
        # move from right
        if y_index != 2:

            temp = copy.deepcopy(self.curr_forw_state)

            temp[x_index][y_index], temp[x_index][y_index + 1] = temp[x_index][y_index + 1], temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.src_expanded:
                self.src_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]

        # move from down
        if x_index != 2:

            temp = copy.deepcopy(self.curr_forw_state)

            temp[x_index][y_index], temp[x_index + 1][y_index] = temp[x_index + 1][y_index], temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.src_expanded:
                self.src_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]
                
        # move from left
        if y_index != 0:

            temp = copy.deepcopy(self.curr_forw_state)

            temp[x_index][y_index], temp[x_index][y_index - 1] = temp[x_index][y_index - 1], temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.src_expanded:
                self.src_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]
                
        self.src_expanded[get_hash(self.curr_forw_state)] = [copy.deepcopy(self.curr_forw_state), self.src_fringe[get_hash(self.curr_forw_state)][2]] 
        del self.src_fringe[get_hash(self.curr_forw_state)]      

    def expand_node_backw_search(self):
        x_index, y_index = -1, -1

        for i in range(3):
            for j in range(3):
                if self.curr_backw_state[i][j] == 0:
                    x_index = i 
                    y_index = j 

        parent_hash_val = get_hash(self.curr_backw_state)

        # move from up
        if x_index != 0:
            
            temp = copy.deepcopy(self.curr_backw_state)
            
            temp[x_index][y_index], temp[x_index - 1][y_index] = temp[x_index - 1][y_index],temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.dest_expanded:
                self.dest_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]

        # move from right
        if y_index != 2:

            temp = copy.deepcopy(self.curr_backw_state)

            temp[x_index][y_index], temp[x_index][y_index + 1] = temp[x_index][y_index + 1], temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.dest_expanded:
                self.dest_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]

        # move from down
        if x_index != 2:

            temp = copy.deepcopy(self.curr_backw_state)

            temp[x_index][y_index], temp[x_index + 1][y_index] = temp[x_index + 1][y_index], temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.dest_expanded:
                self.dest_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]
                
        # move from left
        if y_index != 0:

            temp = copy.deepcopy(self.curr_backw_state)

            temp[x_index][y_index], temp[x_index][y_index - 1] = temp[x_index][y_index - 1], temp[x_index][y_index]

            hash_val = get_hash(temp)

            if hash_val not in self.dest_expanded:
                self.dest_fringe[hash_val] = [compute_manhattan_distance(temp, self.goal_state), copy.deepcopy(temp), parent_hash_val]
        
        self.dest_expanded[get_hash(self.curr_backw_state)] = [copy.deepcopy(self.curr_backw_state), self.dest_fringe[get_hash(self.curr_backw_state)][2]]
        del self.dest_fringe[get_hash(self.curr_backw_state)]

    def change_state_forw_search(self):
        closest_state_hash_val = -1
        min_manhattan_distance = 9999

        for i in self.src_fringe:
            if self.src_fringe[i][0] < min_manhattan_distance:
                min_manhattan_distance = self.src_fringe[i][0]
                closest_state_hash_val = i 
        
        self.curr_forw_state = copy.deepcopy(self.src_fringe[closest_state_hash_val][1])

    def change_state_backw_search(self):
        closest_state_hash_val = -1
        min_manhattan_distance = 999999

        for i in self.dest_fringe:
            if self.dest_fringe[i][0] < min_manhattan_distance:
                min_manhattan_distance = self.dest_fringe[i][0]
                closest_state_hash_val = i 
        
        self.curr_backw_state = copy.deepcopy(self.dest_fringe[closest_state_hash_val][1])

    def print_path(self):
        hash_val = self.intersection_node_hash_val

        while hash_val != -1:
            self.src_path.append(self.src_expanded[hash_val])
            # print(self.src_expanded[hash_val])
            hash_val = self.src_expanded[hash_val][1]

        hash_val = self.intersection_node_hash_val
        
        while hash_val != -1:
            self.dest_path.append(self.dest_expanded[hash_val])
            # print(self.dest_expanded[hash_val])
            hash_val = self.dest_expanded[hash_val][1]

        for i in self.src_path[::-1]:
            print(i)

        for i in self.dest_path[1:]:
            print(i)

    def search(self):

        self.curr_forw_state = copy.deepcopy(self.start_state)
        self.curr_backw_state = copy.deepcopy(self.goal_state)

        self.src_fringe[get_hash(self.curr_forw_state)] = [compute_manhattan_distance(self.curr_forw_state, self.goal_state), self.curr_forw_state, -1]
        self.dest_fringe[get_hash(self.curr_backw_state)] = [compute_manhattan_distance(self.curr_backw_state, self.start_state), self.curr_backw_state, -1]

        while not self.intersecting_nodes():

            self.expand_node_forw_search()
            self.change_state_forw_search()

            self.expand_node_backw_search()
            self.change_state_backw_search()

        self.print_path()


exp = Bi_directional_search()
exp.take_states()
if exp.validate_start_state():
    exp.search() 

