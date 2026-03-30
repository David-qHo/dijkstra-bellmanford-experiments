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
        self.values = {} # Store tuples of longitude and latitude 

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


    


wg = WeightedGraph() 
wg.add_node(1,(3,4))
wg.add_node(2,(4,5))

wg.add_edge(1,2,100) 
print(wg.number_of_nodes())

print(wg.adj)
print(wg.values)



# From one source station, create a function/dictionary 
# which takes in another station and returns the straight line distance
#  from this station to the source station 
# Compute heuristic from every node to that destination (target)
class HeuristicGraph: 
    
    def __init__(self, target): 
        self.target = target  # Initialize source for this heuristic
        self.heuristic = {}   # Initialize dictionary


    def get_heuristic(): 
        return  

    

    def compute_dist(target): 
        return 
    


def compute_heurstic(G,target): 
    return 