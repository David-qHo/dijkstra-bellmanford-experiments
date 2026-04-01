import math 
import min_heap

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
            self.heuristic[node] = math.sqrt((self.values[target][0] - self.values[node][0])**2 + (self.values[target][1] - self.values[node][1])**2)

        


# hg = HeuristicGraph(compute_heuristic(G,target))

# Own the graph and the algorithm
# So create the specific object you need inside here 
class ShortPathFinder: 

    # graph is expecting instance of Graph
    # algorithm is expecting instance of SPAlgorithm
    def __init__(self,graph, algorithm): 
        if(isinstance(graph,Graph) and isinstance(algorithm,SPAlgorithm)):
            self.g = graph 
            self.alg = algorithm 

    # Use algorithms shortest path method 
    def calc_short_path(self, source, dest): 
        return self.alg.calc_sp(self.g,source,dest)
    
    # Update graph
    def set_graph(self, graph): 
        if(isinstance(graph,Graph)):
            self.g = graph 

    # Update algorithm, expecting instanceof SPAlgorithm 
    def set_algorithm(self,algorithm):
        if(isinstance(algorithm,SPAlgorithm)):
            self.alg = algorithm 




# Abstract class
class SPAlgorithm:

    def __init__(self): 
        pass 

    # Override method in subclasses
    def calc_sp(self,graph, source, dest): 
        pass


# Shortest path algorithms
class Dijkstra(SPAlgorithm): 

    def __init__(self): 
        pass 

    # Run dijkstra, but only return for specific target
    def calc_sp(self, G, source, dest):
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
        return dist[dest]
    



class Bellman_Ford(SPAlgorithm): 

    def __init__(): 
        pass 

    # Override 
    def calc_sp(self, G, source, dest):
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

        return dist[dest] # Return shortest path to destination 
    
class A_star(SPAlgorithm): 

    def __init__(self,h): 
        # Store heuristic
        self.h = h
        pass 

    # Override 
    def calc_sp(self, G, source, dest):
        pred = {} 
        dist = {} 
        Q = min_heap.MinHeap([])
        nodes = list(G.adj.keys())

        for node in nodes:
            dist[node] = float("inf")
            priority = float("inf") if node != source else self.h[source]
            Q.insert(min_heap.Element(node, priority))
        
        dist[source] = 0

        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            
            if current_node == dest:
                break

            for neighbour in G.adj[current_node]:
                new_g = dist[current_node] + G.w(current_node, neighbour)
                
                if new_g < dist[neighbour]:
                    dist[neighbour] = new_g
                    pred[neighbour] = current_node
                    f_score = new_g + self.h[neighbour]
                    Q.decrease_key(neighbour, f_score)

        path = []
        curr = dest
        while curr in pred:
            path.append(curr)
            curr = pred[curr]
        if curr == source:
            path.append(source)
        
        path.reverse()
        
        return pred, path



