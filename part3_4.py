import math 

#Undirected graph using an adjacency list
class Graph:
    def __init__(self, n):
        self.adj = {}
        for i in range(1,n+1):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    def number_of_nodes(self):
        return len(self.adj)
    

class WeightedGraph(Graph):

    def __init__(self):
        self.adj = {}
        self.weights = {} 
        self.values = {} # Store tuples of (latitude,longitude) 

    # Get weight between node1 and node2
    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]
        
     # Override node function
    def add_node(self,node,value): 
        self.adj[node] = [] 
        self.values[node] = value

    # override add_edge function 
    def add_edge(self, node1, node2, weight):
        # Undirected graph
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)
    
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight


    


# wg = WeightedGraph() 
# wg.add_node(1,(3,4))
# wg.add_node(2,(4,5))

# wg.add_edge(1,2,100) 
# print(wg.number_of_nodes())

# print(wg.adj)
# print(wg.values)



# From one source station, create a function/dictionary 
# which takes in another station and returns the straight line distance
#  from this station to the source station 
# Compute heuristic from every node to that destination (target)
class HeuristicGraph(WeightedGraph): 
    
    # Takes a weighted graph and target as argument
    def __init__(self,n): 
        super().__init__()
        self.heuristic = {}   # Initialize dictionary


        for i in range(1,n+1): 
            self.heuristic[i] = float("inf")


    def get_heuristic(self): 
        return self.heuristic
    

    def compute_heuristic(self,target): 
        #calculates the euclidian distance from each node to the target node and returns a hueristic function
        for node in list(self.adj.keys()):
            self.heuristic[node] = math.sqrt((self.values[target][0] - G.values[node][0])**2 + (self.values[target][1] - self.values[node][1])**2)

        


# hg = HeuristicGraph(compute_heuristic(G,target))

# Own the graph and the algorithm
# So create the specific object you need inside here 
class ShortPathFinder: 

    pass 


