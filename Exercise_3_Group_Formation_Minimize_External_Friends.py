import random

class SocialNetworkPartition:
    def __init__(self, adjacency_list):
        self.graph = adjacency_list
        self.nodes = list(adjacency_list.keys())
        self.N = len(self.nodes)
        self.min_group_size = int(0.4 * self.N)  # 40% minimum per group

    def count_cross_edges(self, group_a, group_b):
        cross = 0
        group_b_set = set(group_b)
        for user in group_a:
            for friend in self.graph[user]:
                if friend in group_b_set:
                    cross += 1
        return cross

    def is_balanced(self, group_a, group_b):
        return len(group_a) >= self.min_group_size and len(group_b) >= self.min_group_size

    def find_balanced_partition_greedy(self):
        if self.N == 0:
            return (0, [], [])

        shuffled = self.nodes.copy()
        random.shuffle(shuffled)
        split_idx = random.randint(self.min_group_size, self.N - self.min_group_size)
        group_a = shuffled[:split_idx]
        group_b = shuffled[split_idx:]

        improved = True
        while improved:
            improved = False
            for node in self.nodes:
                # Try moving node to the other group
                new_a = group_a.copy()
                new_b = group_b.copy()
                if node in new_a:
                    new_a.remove(node)
                    new_b.append(node)
                else:
                    new_b.remove(node)
                    new_a.append(node)

                if self.is_balanced(new_a, new_b):
                    old_cross = self.count_cross_edges(group_a, group_b)
                    new_cross = self.count_cross_edges(new_a, new_b)
                    if new_cross < old_cross:
                        group_a, group_b = new_a, new_b
                        improved = True

        cross_count = self.count_cross_edges(group_a, group_b)
        return (cross_count, group_a, group_b)

    def find_balanced_partition_local_search(self, iterations=10):
        best_cross = float('inf')
        best_a = []
        best_b = []

        for _ in range(iterations):
            cross, a, b = self.find_balanced_partition_greedy()
            if cross < best_cross:
                best_cross = cross
                best_a = a
                best_b = b

        return (best_cross, best_a, best_b)


def run_tests():
    print("--- Running Exercise 3 Edge Case Tests ---")

    print("\n[Test 1: Empty Graph]")
    net_empty = SocialNetworkPartition({})
    print(f"Greedy Partition: {net_empty.find_balanced_partition_greedy()}")

    print("\n[Test 2: 5 Isolated Nodes]")
    isolated = {0: [], 1: [], 2: [], 3: [], 4: []}
    net_iso = SocialNetworkPartition(isolated)
    print(f"Greedy Partition: {net_iso.find_balanced_partition_greedy()}")

    print("\n[Test 3: Fully Connected K5]")
    k5 = {
        0: [1,2,3,4],
        1: [0,2,3,4],
        2: [0,1,3,4],
        3: [0,1,2,4],
        4: [0,1,2,3]
    }
    net_k5 = SocialNetworkPartition(k5)
    print(f"Greedy: {net_k5.find_balanced_partition_greedy()}")

    print("\n[Test 4: Star Graph]")
    star = {0:[1,2,3,4], 1:[0], 2:[0], 3:[0], 4:[0]}
    net_star = SocialNetworkPartition(star)
    print(f"Greedy: {net_star.find_balanced_partition_greedy()}")

    print("\n[Test 5: Local Search (10 iterations)]")
    test_graph = {0:[1], 1:[0,2], 2:[1,3], 3:[2,4], 4:[3]}
    net_test = SocialNetworkPartition(test_graph)
    print(f"Local Search Result: {net_test.find_balanced_partition_local_search(10)}")


if __name__ == "__main__":
    run_tests()
