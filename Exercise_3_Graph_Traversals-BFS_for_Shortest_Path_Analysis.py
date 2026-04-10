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

    def bfs(self, start):
        from collections import deque
        visited = [False] * self.num_users
        q = deque([start])
        visited[start] = True
        result = []
        while q:
            node = q.popleft()
            result.append(node)
            for neighbor in self.adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    q.append(neighbor)
        return result

    def bfs_distances(self, start):
        from collections import deque
        visited = [False] * self.num_users
        q = deque([start])
        visited[start] = True
        dist = {start: 0}
        while q:
            node = q.popleft()
            for neighbor in self.adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    dist[neighbor] = dist[node] + 1
                    q.append(neighbor)
        return dist

    def shortest_path(self, start, end):
        from collections import deque
        visited = [False] * self.num_users
        q = deque([(start, [start])])
        visited[start] = True
        while q:
            node, path = q.popleft()
            if node == end:
                return path
            for neighbor in self.adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    q.append((neighbor, path + [neighbor]))
        return []

def run_bfs_tests():
    print("=== Start BFS Tests ===")

    print("\n--- Test 1: Basic BFS Traversal ---")
    g1 = SocialGraph(5)
    g1.add_friendship(0, 1)
    g1.add_friendship(0, 2)
    g1.add_friendship(1, 3)
    g1.add_friendship(3, 4)
    print(f"BFS from 0: {g1.bfs(0)}")

    print("\n--- Test 2: BFS Distance Calculation ---")
    print(f"Distances from 0: {g1.bfs_distances(0)}")

    print("\n--- Test 3: Shortest Path ---")
    print(f"Shortest path 0->4: {g1.shortest_path(0, 4)}")

    print("\n=== All BFS tests completed ===")

if __name__ == "__main__":
    run_bfs_tests()
