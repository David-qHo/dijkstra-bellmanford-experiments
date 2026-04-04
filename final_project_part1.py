import min_heap
import random
import matplotlib.pyplot as plt
import math 
from itertools import permutations 
import timeit
import numpy as np
import csv
import part3_4
import os


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

def a_star(G, s, d, h):
    pred = {} 
    dist = {} 
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    for node in nodes:
        dist[node] = float("inf")
        priority = float("inf") if node != s else h[s]
        Q.insert(min_heap.Element(node, priority))
    
    dist[s] = 0

    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        
        if current_node == d:
            break

        for neighbour in G.adj[current_node]:
            new_g = dist[current_node] + G.w(current_node, neighbour)
            
            if new_g < dist[neighbour]:
                dist[neighbour] = new_g
                pred[neighbour] = current_node
                f_score = new_g + h[neighbour]
                Q.decrease_key(neighbour, f_score)

    path = []
    curr = d
    while curr in pred:
        path.append(curr)
        curr = pred[curr]
    if curr == s:
        path.append(s)
    
    path.reverse()
    
    return pred, path


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



def mysteryExperiment():

    min_nodes = 5
    max_nodes = 200
    max_cost = 200
    grapharr = []

    for i in range(min_nodes,max_nodes):
        g = create_random_complete_graph(i,max_cost)
        grapharr.append(g)

    mysteryData = []
    mysteryTotal = 0

    for g in grapharr:
        start = timeit.default_timer()
        mystery(g)
        end = timeit.default_timer() - start
        mysteryTotal += end
        mysteryData.append(end)

    x = np.array(range(min_nodes,max_nodes))
    y = np.array(mysteryData)

    log_x = np.log(x)
    log_y = np.log(y)

    # m here is our slope of the log log plot line
    m, c = np.polyfit(log_x, log_y, 1)


    plt.loglog(range(min_nodes,max_nodes), mysteryData, color='blue')


    plt.xlabel("Number of Graph's Nodes")
    plt.ylabel("Time (s)")
    plt.title("Runtime Analysis of Mystery Function Slope = " + str(m))
    plt.show()

    return


# mysteryExperiment()


# ************* Reading the csv files *************************


base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path 
# Was having issues with relative path
file_path_1 = os.path.join(base_dir, 'data', 'london_stations.csv')
file_path_2 = os.path.join(base_dir, 'data', 'london_connections.csv')


with open(file_path_1, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)

    size = sum(1 for row in file) - 1
    
    g = part3_4.HeuristicGraph(size)

    file.seek(0)

    for row in csv_reader:
        g.add_node(int(row['id']),(float(row['latitude']),float(row['longitude'])))
    

with open(file_path_2, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        g.add_edge(int(row['station1']),int(row['station2']),int(row['time']))




#testing dijsktra's algorithm
# dict1 = dijkstra(g,6)
# dist1 = total_dist(dict1)
# print(dict1)

#testing A* algorithm 
# g.compute_heuristic(303)
# h = g.get_heuristic()
# pred, dict2 = a_star(g,6,303,h)
# print(dict2)


def experiment4():
    distances = []
    dijkstra_times = []
    a_star_times = []
    dijkstra_total = 0
    a_star_total = 0

    for source in range(50,int((size + 1)/2)):

        start = timeit.default_timer()
        dijkstra(g,source)
        end = timeit.default_timer() - start
        dijkstra_total = end

        for target in range(50,int((size + 1)/2)):
            g.compute_heuristic(target)
            h = g.get_heuristic()

            start = timeit.default_timer()
            pred, path = a_star(g,source,target,h)
            end = timeit.default_timer() - start
            a_star_total = end

            total_distance = 0
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i+1]
                total_distance += g.w(u, v)

            dijkstra_times.append(dijkstra_total)
            a_star_times.append(a_star_total)
            distances.append(total_distance)


    plt.figure(figsize=(12, 6))
    
    plt.scatter(distances, dijkstra_times, color='blue', label="Dijkstra", alpha=0.6)
    plt.scatter(distances, a_star_times, color='red', label="A*", alpha=0.6)

    # plt.plot(pairs, dijkstra_times, color='blue', label = "Dijksta")
    # plt.plot(pairs, a_star_times, color='red', label = "A*")

    plt.xlabel("Distance (source to target)")
    plt.ylabel("Times (s)")
    plt.title("Runtime by Distance to Target Node")
    plt.legend()
    plt.show()

def part3_2(g): 

    num_lines = 3
    # Same lines: 
    #Southgate (232) -> Manor house (160)
    #South ruislip (239) -> North acton (181)
    # Wimbledon (299) -> West brompton (287)

    # On adjacent lines: 
    # Adj pair 1: 
    #  Hammersmith(110) -> Westbourne Park(283)
    #  Hammersmith(110) -> Ladbroke grove(147) 
    # Adj pair 2: 
    #  Liverpool St(156) -> Euston Square(90)
    #  Liverpool St(156) -> Great Portland St(104) 
    # Adj pair 3: 
    #  Ealing broadway(72) -> West Kensington(293)
    #  Ealing broadway(72) -> Barons court(17)
    num_adj_lines = 2 # Num of lines per adjacent (Will use to compute average)

    # On lines which require several transfers (At least 2)
    # Queen's Park (206) -> South kensington (236)
    # Bank (13) -> Baker Street(110)
    # Wimbledon(299) -> Bank(13)

    # Store dict of pairs for same/adj/transfer lines
    same_lines = {232: 160, 239: 181, 299: 287}
    adj_lines = {110: [283,147], 156: [90,104], 72: [293,17] }
    transfer_lines = {206: 236, 13: 110, 299: 13}

    # Store total time
    dijkstra_same_t = 0
    dijkstra_adj_t = 0
    dijkstra_transfer_t = 0

    a_star_same_t = 0
    a_star_adj_t = 0
    a_star_transfer_t = 0

    # Store total distancce
    dijkstra_same_dist = 0
    dijkstra_adj_dist = 0
    dijkstra_transfer_dist = 0

    a_star_same_dist = 0
    a_star_adj_dist = 0
    a_star_transfer_dist = 0

    # Same lines computation 

    for source in same_lines.keys(): 
        # print(same_lines[source])
        
        # Dijkstra
        start = timeit.default_timer()
        ds = dijkstra(g,source)
        end = timeit.default_timer() - start
        dijkstra_same_t += end
        dijkstra_same_dist += ds[same_lines[source]] # Add length of this path

        # A_star
        g.compute_heuristic(same_lines[source])
        h = g.get_heuristic()

        start = timeit.default_timer()
        pred, path = a_star(g,source,same_lines[source],h)
        end = timeit.default_timer() - start
        a_star_same_t += end

        # Compute a_star path length
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            a_star_same_dist += g.w(u, v)


    dijkstra_same_dist /= num_lines # Get average total distance
    dijkstra_same_t /= num_lines # Get average time

    a_star_same_dist /= num_lines # Get average total distance
    a_star_same_t /= num_lines # Get average time

    # Get average for each of the pairs of lines 
    # Then compute average of those averages 

    
    for source in adj_lines.keys(): 
        # Reset stuff for every source
        dijkstra_pair_avg_dist = 0
        a_star_pair_avg_dist = 0 

        dijkstra_pair_avg_t = 0
        a_star_pair_avg_t = 0

        # For each pair
        for target in adj_lines[source]:
            # Dijkstra
            start = timeit.default_timer()
            ds = dijkstra(g,source)
            end = timeit.default_timer() - start
            dijkstra_pair_avg_t += end
            dijkstra_pair_avg_dist += ds[target] # Add length of this path

            # A_star
            g.compute_heuristic(target)
            h = g.get_heuristic()

            start = timeit.default_timer()
            pred, path = a_star(g,source,target,h)
            end = timeit.default_timer() - start
            a_star_pair_avg_t += end

            # Compute a_star path length
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i+1]
                a_star_pair_avg_dist += g.w(u, v)

        dijkstra_adj_dist += (dijkstra_pair_avg_dist / 2) # Compute average for this pair
        dijkstra_adj_t += (dijkstra_pair_avg_t / 2) 

        a_star_adj_dist += (a_star_pair_avg_dist / 2) 
        a_star_adj_t += (a_star_pair_avg_t / 2)


    dijkstra_adj_dist /= num_lines # Get average total distance
    dijkstra_adj_t /= num_lines # Get average time

    a_star_adj_dist /= num_lines # Get average total distance
    a_star_adj_t /= num_lines # Get average time



    # Transfer lines
    for source in transfer_lines.keys(): 
        
        # Dijkstra
        start = timeit.default_timer()
        ds = dijkstra(g,source)
        end = timeit.default_timer() - start
        dijkstra_transfer_t += end
        dijkstra_transfer_dist += ds[transfer_lines[source]] # Add length of this path

        # A_star
        g.compute_heuristic(transfer_lines[source])
        h = g.get_heuristic()

        start = timeit.default_timer()
        pred, path = a_star(g,source,transfer_lines[source],h)
        end = timeit.default_timer() - start
        a_star_transfer_t += end

        # Compute a_star path length
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            a_star_transfer_dist += g.w(u, v)


    dijkstra_transfer_dist /= num_lines # Get average total distance
    dijkstra_transfer_t /= num_lines # Get average time

    a_star_transfer_dist /= num_lines # Get average total distance
    a_star_transfer_t /= num_lines # Get average time

    # For same source dijkstra will be the same

    # Print results 

    # Same line 
    print("Same line data:")
    print(f"Dijkstra Same line (weight): {round(dijkstra_same_dist,4)}")
    print(f"Dijksttra Same line (runtime): {round(dijkstra_same_t * 1000,4)}ms")

    print(f"A_star Same line (weight): {round(a_star_same_dist,4)}")
    print(f"A_star Same line (runtime): {round(a_star_same_t * 1000,4)}ms")
    print("\n")

    # Adj line 
    print("Adjacent line data:")
    print(f"Dijkstra Adj line (weight): {round(dijkstra_adj_dist,4)}")
    print(f"Dijksttra Adj line (runtime): {round(dijkstra_adj_t * 1000,4)}ms")

    print(f"A_star Adj line (weight): {round(a_star_adj_dist,4)}")
    print(f"A_star Adj line (runtime): {round(a_star_adj_t * 1000,4)}ms")
    print("\n")

    # Transfer lines
    print("Transfer data:")
    print(f"Dijkstra Transfer (weight): {round(dijkstra_transfer_dist,4)}")
    print(f"Dijksttra Transfer (runtime): {round(dijkstra_transfer_t * 1000,4)}ms")

    print(f"A_star Transfer (weight): {round(a_star_transfer_dist,4)}")
    print(f"A_star Transfer (runtime): {round(a_star_transfer_t * 1000,4)}ms")



part3_2(g)
