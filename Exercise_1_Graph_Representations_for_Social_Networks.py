class SocialGraph:
    def __init__(self, num_users):
        self.num_users = num_users
        self.num_edges = 0
        
        # Adjacency Matrix
        self.matrix = [[False] * num_users for _ in range(num_users)]
        
        # Adjacency List
        self.adj_list = [[] for _ in range(num_users)]

    def add_friendship(self, u, v):
        if u != v and not self.matrix[u][v]:
            self.matrix[u][v] = True
            self.matrix[v][u] = True
            
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            
            self.num_edges += 1

    def remove_friendship(self, u, v):
        if self.matrix[u][v]:
            self.matrix[u][v] = False
            self.matrix[v][u] = False
            
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)
            
            self.num_edges -= 1

    def are_friends_matrix(self, u, v):
        return self.matrix[u][v]

    def are_friends_list(self, u, v):
        return v in self.adj_list[u]

    def get_friends_matrix(self, u):
        return [i for i, is_friend in enumerate(self.matrix[u]) if is_friend]

    def get_friends_list(self, u):
        return self.adj_list[u]

    def get_degree(self, u):
        return len(self.adj_list[u])

    def get_num_users(self):
        return self.num_users

    def get_num_edges(self):
        return self.num_edges

    def is_complete_graph(self):
        if self.num_users <= 1:
            return True
        max_possible_edges = self.num_users * (self.num_users - 1) // 2
        return self.num_edges == max_possible_edges

    def graph_density(self):
        if self.num_users <= 1:
            return 0.0 
        return (2 * self.num_edges) / (self.num_users * (self.num_users - 1))

    def degree_distribution(self):
        distribution = {}
        for u in range(self.num_users):
            deg = self.get_degree(u)
            distribution[deg] = distribution.get(deg, 0) + 1
        return distribution

    def matrix_to_list(self):
        new_list = [[] for _ in range(self.num_users)]
        for u in range(self.num_users):
            for v in range(self.num_users):
                if self.matrix[u][v]:
                    new_list[u].append(v)
        self.adj_list = new_list

    def list_to_matrix(self):
        new_matrix = [[False] * self.num_users for _ in range(self.num_users)]
        for u in range(self.num_users):
            for v in self.adj_list[u]:
                new_matrix[u][v] = True
        self.matrix = new_matrix

def run_edge_tests():
    print("=== Start Edge Tests ===")

    print("\n--- Test 1: Single User Network ---")
    g1 = SocialGraph(1)
    print(f"Expected density: 0.0, Actual density: {g1.graph_density()}")
    print(f"Expected complete graph: True, Actual: {g1.is_complete_graph()}")

    print("\n--- Test 2: Exceptional Addition and Removal ---")
    g2 = SocialGraph(3)
    g2.add_friendship(0, 1)
    g2.add_friendship(0, 1) # Trying to add the same edge again
    g2.add_friendship(2, 2) # Trying to add a self-loop (user adding themselves)
    print(f"Duplicate additions and self-loops (Expected: 1): {g2.get_num_edges()}")
    
    g2.remove_friendship(0, 2) # Trying to remove a non-existent relationship
    print(f"Edges after attempting to remove non-existent edge (Expected: 1): {g2.get_num_edges()}")

    print("\n--- Test 3: Complete Graph Properties Test ---")
    g3 = SocialGraph(4)
    for i in range(4):
        for j in range(i + 1, 4):
            g3.add_friendship(i, j)
            
    print(f"Current number of edges (Expected: 6): {g3.get_num_edges()}")
    print(f"Is complete graph (Expected: True): {g3.is_complete_graph()}")
    print(f"Graph density (Expected: 1.0): {g3.graph_density()}")
    print(f"Degree distribution (Expected: { {3: 4} }): {g3.degree_distribution()}")

    print("\n--- Test 4: Matrix and List Data Conversion ---")
    g3.adj_list = [[] for _ in range(4)]
    g3.matrix_to_list()
    print(f"Destroyed adjacency list and restored from matrix, degree of user 0 (Expected: 3): {g3.get_degree(0)}")
    
    g3.matrix = [[False] * 4 for _ in range(4)]
    g3.list_to_matrix()
    print(f"Destroyed matrix and restored from adjacency list, are users 0 and 3 friends (Expected: True): {g3.are_friends_matrix(0, 3)}")
    
    print("\n=== All edge tests completed ===")

if __name__ == "__main__":
    run_edge_tests()
