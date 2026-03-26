import min_heap
import random
import matplotlib.pyplot as plt

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

            #  G.w(n1, n2) returns the weight of edge from n1 -> n2
            # If this new path is less than the current path (dist[neighbour]) 
            #   - replace it 
            # This is the relaxation 
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                if num_relax[neighbour] > 0: # There is still available room to relax this node 
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

                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    if num_relax[neighbour] > 0:  # Still available room to relax this node
                        num_relax[neighbour] -= 1
                        dist[neighbour] = dist[node] + G.w(node, neighbour)
                        pred[neighbour] = node
    return dist


# g = DirectedWeightedGraph()

# g.add_node(0) 
# g.add_node(1)
# g.add_node(2) 

# g.add_edge(0,1,1)
# g.add_edge(0,2,100)
# g.add_edge(1,2,1)

# print(dijkstra_approx(g,0,30000))



# Experiments what to vary
# number of nodes n
# graph density / number of edges m
# relaxation limit k
# outcome measure: runtime, total_dist(dist), or error vs the exact algorithm

# How number of nodes affects approximations 
# Fix number of relaxations to some k, and number of edges to some m
# To fix edges use complete random graph function
def experiment1(): 

    # 1000 graphs, sizes from 1 to 1000 

    max_nodes = 100 
    num_graphs = 5


    graphs = {}
    for i in range(1,max_nodes+1): 
        graphs[i] = [] # initialize empty graphs 
        for _ in range(num_graphs): # Make 5 graphs for every number of nodes
            graphs[i].append(create_random_complete_graph(i,2 * i))

    # Compute average total_dist of all 5 graphs
        
        
    total_dists_dijkstra = []
    total_dists_bellman= []


    # Put max weight as twice number of nodes, avoid duplicates
    for i in range(1,max_nodes,10): 
        graphs.append(create_random_complete_graph(i,2 * i))


    for graph in graphs: 
        total_dists_dijkstra.append(total_dist(dijkstra_approx(graph,0,)))


    print(graphs) 


def experiment3(): 

    max_nodes = 20
    max_cost = 60
    number_graphs = 5
    grapharr = []

    for i in range(number_graphs):
        g = create_random_complete_graph(max_nodes,max_cost)
        grapharr.append(g)

    
    # Compute average total_dist of all 10 graphs
    total_dists_dijkstra = []
    total_dists_bellman= []
    total_dists_actual= []


    for k in range(1,20):
        sum1, sum2, sum3 = 0, 0, 0
        for graph in grapharr: 
            sum1 += total_dist(dijkstra_approx(graph,0,k))
        total_dists_dijkstra.append(sum1/number_graphs)

        for graph in grapharr: 
            sum2 += total_dist(bellman_ford_approx(graph,0,k))
        total_dists_bellman.append(sum2/number_graphs)


    for graph in grapharr: 
        sum3 += total_dist(dijkstra(graph,0,))

    for k in range (1,20):
        total_dists_actual.append(sum3/number_graphs)


    plt.plot(range(1,20), total_dists_dijkstra, color='blue', label = "Dijksta Approx")
    plt.plot(range(1,20), total_dists_bellman, color='red', label = "Bellman Approx")
    plt.plot(range(1,20), total_dists_actual, color='green', label = "Actual")

    plt.xlabel("K values")
    plt.ylabel("Distance")
    plt.title("Minimum Distance Approximations by K Value")
    plt.legend()
    plt.show()

    print(total_dists_dijkstra) 
    print(total_dists_bellman) 
    print(total_dists_actual) 




experiment3()