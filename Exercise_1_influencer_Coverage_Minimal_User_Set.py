import itertools

class SocialNetwork:
    def __init__(self, adjacency_list):
        self.graph = adjacency_list
        self.nodes = list(adjacency_list.keys())
        self.N = len(self.nodes)

    def is_valid_coverage(self, selected_users):
        """
        Validate if the selected users form a valid coverage set.  
        """
        covered = set(selected_users)
        for user in selected_users:
            if user in self.graph:
                covered.update(self.graph[user])
        
        return len(covered) == self.N

    def find_minimum_coverage(self):
        for size in range(1, self.N + 1):
            for subset in itertools.combinations(self.nodes, size):
                if self.is_valid_coverage(subset):
                    return (size, list(subset))
        return (0, [])

    def find_fast_coverage(self):
        uncovered = set(self.nodes)
        selected_users = []
        
        while uncovered:
            best_node = None
            max_newly_covered = -1
            
            for node in self.nodes:
                coverage_set = {node}.union(set(self.graph[node]))
                newly_covered_count = len(coverage_set.intersection(uncovered))
                
                if newly_covered_count > max_newly_covered:
                    max_newly_covered = newly_covered_count
                    best_node = node
            
            if best_node is None: break
            
            selected_users.append(best_node)
            coverage_set = {best_node}.union(set(self.graph[best_node]))
            uncovered -= coverage_set
            
        return (len(selected_users), selected_users)
    
def run_tests():
    print("--- Running Exercise 1 Edge Case Tests ---")

    # 1. Empty Graph - No nodes
    print("\n[Test 1: Empty Graph]")
    net_empty = SocialNetwork({})
    print(f"Min Coverage: {net_empty.find_minimum_coverage()}")
    print(f"Fast Coverage: {net_empty.find_fast_coverage()}")

    # 2. Sparse Graph - Isolated Nodes
    print("\n[Test 2: Sparse Graph - Isolated Nodes]")
    net_isolated = SocialNetwork({0: [], 1: [], 2: []})
    print(f"Min Coverage: {net_isolated.find_minimum_coverage()}")

    # 3. Fully Connected Graph
    print("\n[Test 3: Fully Connected Graph (K4)]")
    k4 = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2]
    }
    net_k4 = SocialNetwork(k4)
    print(f"Min Coverage: {net_k4.find_minimum_coverage()}")
    print(f"Fast Coverage: {net_k4.find_fast_coverage()}")

    # 4. Star Graph
    print("\n[Test 4: Star Graph (Center covers all)]")
    star = {
        0: [1, 2, 3, 4],
        1: [0], 2: [0], 3: [0], 4: [0]
    }
    net_star = SocialNetwork(star)
    print(f"Min Coverage (Should be size 1): {net_star.find_minimum_coverage()}")
    print(f"Fast Coverage: {net_star.find_fast_coverage()}")

    # 5. Counter-example
    print("\n[Test 5: Greedy Counter-example]")
    graph_ce = {
        'A': ['L1', 'L2'],
        'B': ['L3', 'L4'],
        'C': ['L1', 'L2', 'L3', 'L4'],
        'L1': ['A', 'C'], 'L2': ['A', 'C'],
        'L3': ['B', 'C'], 'L4': ['B', 'C']
    }
    net_ce = SocialNetwork(graph_ce)
    print(f"Exact Min: {net_ce.find_minimum_coverage()}")
    print(f"Greedy Result: {net_ce.find_fast_coverage()}")

if __name__ == "__main__":
    run_tests()