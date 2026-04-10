class SocialGraph:
    def __init__(self, num_users):
        self.num_users = num_users
        self.num_edges = 0
        self.matrix = [[False] * num_users for _ in range(num_users)]
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

    def dfs_recursive(self, start):
        visited = [False] * self.num_users
        result = []

        def dfs(node):
            visited[node] = True
            result.append(node)
            for neighbor in self.adj_list[node]:
                if not visited[neighbor]:
                    dfs(neighbor)

        dfs(start)
        return result

    def dfs_iterative(self, start):
        visited = [False] * self.num_users
        stack = [start]
        result = []
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                result.append(node)
                for neighbor in reversed(self.adj_list[node]):
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return result

    def find_connected_components(self):
        visited = [False] * self.num_users
        components = []
        for user in range(self.num_users):
            if not visited[user]:
                comp = self.dfs_iterative(user)
                components.append(comp)
                for n in comp:
                    visited[n] = True
        return components

    def is_connected(self):
        return len(self.find_connected_components()) == 1

    def has_path(self, start, end):
        visited = [False] * self.num_users
        stack = [start]
        while stack:
            node = stack.pop()
            if node == end:
                return True
            if not visited[node]:
                visited[node] = True
                for neighbor in self.adj_list[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return False

def run_dfs_tests():
    print("=== Start DFS Tests ===")

    print("\n--- Test 1: Basic DFS Traversal ---")
    g1 = SocialGraph(5)
    g1.add_friendship(0, 1)
    g1.add_friendship(0, 2)
    g1.add_friendship(1, 3)
    g1.add_friendship(3, 4)
    print(f"DFS Recursive from 0: {g1.dfs_recursive(0)}")
    print(f"DFS Iterative from 0: {g1.dfs_iterative(0)}")

    print("\n--- Test 2: Connected Components ---")
    g2 = SocialGraph(6)
    g2.add_friendship(0, 1)
    g2.add_friendship(2, 3)
    g2.add_friendship(4, 5)
    print(f"Connected Components: {g2.find_connected_components()}")
    print(f"Is Graph Connected: {g2.is_connected()}")

    print("\n--- Test 3: Path Existence Check ---")
    print(f"Has path 0->3: {g1.has_path(0, 3)}")
    print(f"Has path 0->5: {g2.has_path(0, 5)}")

    print("\n=== All DFS tests completed ===")

if __name__ == "__main__":
    run_dfs_tests()
