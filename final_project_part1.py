import min_heap
import random
import matplotlib.pyplot as plt
import math 
from itertools import permutations 


class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist

# Compute total 'cost' of traversing graph from source
def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper)) # Add edge between i, j with random weight 
    return G


#Assumes G represents its nodes as integers 0,1,...,(n-1)
# Graph it, come to some conclusions about it 
# Test with negative edges, and positive edges 
# Test with negative cycles 
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d


# ******* OUR CODE ******* # 


# Relax each node at most k times
def dijkstra_approx(G, source,k):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    num_relax = {} # Store amount each node is able to be relaxed

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf"))) # Set all other nodes to inf
        dist[node] = float("inf")

        # Set each nodes limit to being relaxed 
        num_relax[node] = k


    Q.decrease_key(source, 0) # Set source to be value 0

    #Meat of the algorithm
    # Min heap elements: (value,key) -> (node,cost)
    while not Q.is_empty():
        current_element = Q.extract_min() # Get min cost node
        current_node = current_element.value     # Get node 
        dist[current_node] = current_element.key # Get cost 
        for neighbour in G.adj[current_node]:    # For all of the nodes neighbours 
            if num_relax[neighbour] > 0: # There is still available room to relax this node 

            #  G.w(n1, n2) returns the weight of edge from n1 -> n2
            # If this new path is less than the current path (dist[neighbour]) 
            #   - replace it 
            # This is the relaxation 
                if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                    # if num_relax[neighbour] > 0: # There is still available room to relax this node 
                        num_relax[neighbour] -= 1 
                        # Update neighbour node with new shortest distance 
                        Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                        dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                        pred[neighbour] = current_node
    return dist

# Relax each node at most k times
def bellman_ford_approx(G, source,k):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    num_relax = {} # Store amount each node can be relaxed
 
    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        num_relax[node] = k 
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if num_relax[neighbour] > 0: # Still available to relax this node
                    if dist[neighbour] > dist[node] + G.w(node, neighbour):
                        # if num_relax[neighbour] > 0:  # Still available room to relax this node
                            num_relax[neighbour] -= 1
                            dist[neighbour] = dist[node] + G.w(node, neighbour)
                            pred[neighbour] = node
    return dist

# Return a graph with n nodes and m edges with upper limit weight upper
# Limited to i CHOOSE 2 edges; since unique edges
def create_random_graph(n,m,upper): 
    G = DirectedWeightedGraph()

    # More edges than possible connections in graph
    # Return empty graph
    if m > (n * (n - 1)):
        return G
    
    for i in range(n):
        G.add_node(i)


    # Calculate all possible pairs of nodes, ignore duplicates (u,v) , (v,u) 
    #  Will only include one of those pairs
    # Also ignores self loops 
    subset = list(permutations([k for k in range(n)],2)) 
                                    
    s = set() # Store pairs of edges (Used to avoid duplicates)

    k = 0 


    # Choose j random edges
    while k < m: 
        choice = random.choice(subset) # Choose random pair of edges

        # Check if choice in s
        if choice not in s: 
            s.add(choice)
            G.add_edge(choice[0],choice[1],random.randint(1,upper))
            k += 1
    
    return G
    

# g = DirectedWeightedGraph()

# g.add_node(0) 
# g.add_node(1)
# g.add_node(2) 

# g.add_edge(0,1,1)
# g.add_edge(0,2,100)
# g.add_edge(1,2,1)

# print(dijkstra(g,1))
# print(bellman_ford(g,1))





# Experiments what to vary
# number of nodes n
# graph density / number of edges m
# relaxation limit k
# outcome measure: runtime, total_dist(dist), or error vs the exact algorithm

# How number of nodes affects approximations 
# Fix number of relaxations to some k, and number of edges to some m
# To fix edges use complete random graph function
def experiment1(): 

    max_nodes = 150  # Max number of nodes
    num_graphs = 5   # Number of graphs per # of nodes

 

    graphs = {}
    x = [] 
    for i in range(1,max_nodes+1,5): 
        x.append(i)
        graphs[i] = [] # initialize empty graphs 
        for _ in range(num_graphs): # Make 5 graphs for every number of nodes
            # Put max-weight as 2 * # of nodes, avoid duplicates
            graphs[i].append(create_random_complete_graph(i,2 * i)) 

    # Compute average total_dist of all 5 graphs
        
        
    td_dij_app = []  # Store approximation of dijkstra
    td_bel_app = []   # Store approximation of bellman

    td_short = []       # Store actual cost of shortest path
    # td_bel = []       # Store actual cost of shortest path

    # key represents number of nodes
    for key in graphs.keys(): # For each number of nodes
        # num_nodes = graphs[key][0].number_of_nodes() # Get number of nodes for this graph

        # Initialize sums for this graph size
        dij_appS = 0 
        bel_appS = 0 
        shortestS = 0 
        # belS = 0

        for graph in graphs[key]: # For each graph in this 
            # Compute approximation 
            dij_appS += total_dist(dijkstra_approx(graph,0, 10)) 
            bel_appS += total_dist(bellman_ford_approx(graph,0, 10))

            # Compute actual 
            shortestS += total_dist(dijkstra(graph,0))
            # belS += total_dist(bellman_ford(graph,0))

        # Divide by num_graphs to compute average
        td_dij_app.append(dij_appS/num_graphs)
        td_bel_app.append(bel_appS/num_graphs)
        td_short.append(shortestS/num_graphs)
        # td_bel.append(belS/num_graphs)

    
    plt.plot(x,td_dij_app, label = "Dijkstra Approx")
    plt.plot(x,td_bel_app, label = "Bellman Approx")
    plt.plot(x,td_short, label = "Actual")
    # plt.plot(x,td_bel, label = "Bellman-Ford")


    plt.xlabel("Number of nodes")
    plt.ylabel("total distance")
    plt.title("Shortest path algorithms and their approximations (k = 10)")
    plt.legend()

    plt.show()
        
    print(td_dij_app) 
    print(td_bel_app)



# Vary number of edges and see how that impacts approximations 
def experiment2(): 
    nodes = 50      # Number of nodes for every graph 
    max_edges = nodes * (nodes - 1) # Max number of edges (n Choose 2)
    num_graphs = 5   # Number of graphs per # of edges

 

    graphs = {} 
    x = [] 

  

    for i in range(1,max_edges,100): 
        # print(f"Generating {i}")
        x.append(i)
        graphs[i] = [] # initialize empty graphs 
        for _ in range(num_graphs): # Make 5 graphs for every number of nodes
            # Put max-weight as 2 * # of nodes, avoid duplicates
            graphs[i].append(create_random_graph(nodes,i, 2 * nodes)) 


    # Compute average total_dist of all 5 graphs
        
        
    td_dij_app = []  # Store approximation of dijkstra
    td_bel_app = []   # Store approximation of bellman

    td_short = []       # Store actual cost of shortest path
    # td_bel = []       # Store actual cost of shortest path

    print(graphs.keys())
    # key represents number of edges
    for key in graphs.keys(): # For each number of nodes
        # print(f"Doing edge: {key}")
        

        # Initialize sums for this graph size
        dij_appS = 0 
        bel_appS = 0 
        shortestS = 0 
        # belS = 0

        for graph in graphs[key]: # For each graph in this 
            # Compute approximation 
            dij_appS += total_dist(dijkstra_approx(graph,0, 10)) 
            bel_appS += total_dist(bellman_ford_approx(graph,0, 10))

            # Compute actual 
            shortestS += total_dist(dijkstra(graph,0))

        # Divide by num_graphs to compute average
        td_dij_app.append(dij_appS/num_graphs)
        td_bel_app.append(bel_appS/num_graphs)
        td_short.append(shortestS/num_graphs)

    
    plt.plot(x,td_dij_app, label = "Dijkstra Approx")
    plt.plot(x,td_bel_app, label = "Bellman Approx")
    plt.plot(x,td_short, label = "Actual")
    # plt.plot(x,td_bel, label = "Bellman-Ford")


    plt.xlabel("Number of edges")
    plt.ylabel("total distance")
    plt.title("Shortest path algorithms and their approximations (k = 10)")
    plt.legend()

    plt.show()
        
    print(td_dij_app) 
    print(td_bel_app)





experiment2()