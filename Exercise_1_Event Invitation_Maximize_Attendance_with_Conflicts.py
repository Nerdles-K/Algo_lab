import copy

class EventOrganizer:
    def __init__(self, adjacency_list):
        self.graph = adjacency_list
        self.nodes = list(adjacency_list.keys())

    def is_valid_invitation(self, invited):
        n = len(invited)
        for i in range(n):
            for j in range(i + 1, n):
                if invited[j] in self.graph[invited[i]]:
                    return False
        return True

    def find_max_invitations_exact(self):
        best_set = []

        def backtrack(index, current_set):
            nonlocal best_set
            
            if len(current_set) + (len(self.nodes) - index) <= len(best_set):
                return
                
            if index == len(self.nodes):
                if len(current_set) > len(best_set):
                    best_set = current_set.copy()
                return

            current_node = self.nodes[index]

            current_set.append(current_node)
            if self.is_valid_invitation(current_set):
                backtrack(index + 1, current_set)
            current_set.pop() 

            backtrack(index + 1, current_set)

        backtrack(0, [])
        return len(best_set), best_set

    def find_max_invitations_greedy(self):
        working_graph = copy.deepcopy(self.graph)
        invited_list = []

        while working_graph:
            min_node = min(working_graph.keys(), key=lambda n: len(working_graph[n]))
            invited_list.append(min_node)
            
            to_remove = [min_node] + working_graph[min_node]
            
            for node in to_remove:
                if node in working_graph:
                    for neighbor in working_graph[node]:
                        if neighbor in working_graph:
                            working_graph[neighbor].remove(node)
                    del working_graph[node]

        return len(invited_list), invited_list
    
def run_tests():
    print("--- Running Exercise 1 Edge Case Tests ---")

    # Empty Graph - No conflicts, no users
    print("\n[Test 1: Empty Graph]")
    org_empty = EventOrganizer({})
    print(f"Exact Max: {org_empty.find_max_invitations_exact()}")

    # Isolated Nodes
    print("\n[Test 2: No Conflicts (Everyone can be invited)]")
    org_isolated = EventOrganizer({
        'A': [], 'B': [], 'C': []
    })
    print(f"Exact Max: {org_isolated.find_max_invitations_exact()}")
    print(f"Greedy Max: {org_isolated.find_max_invitations_greedy()}")

    # Fully Connected - Everyone conflicts with everyone
    print("\n[Test 3: Fully Connected (Can only invite 1 person)]")
    org_clique = EventOrganizer({
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['A', 'B', 'C']
    })
    print(f"Exact Max: {org_clique.find_max_invitations_exact()}")
    print(f"Greedy Max: {org_clique.find_max_invitations_greedy()}")

    # Greedy Counterexample
    print("\n[Test 4: Greedy Counterexample]")
    graph_ce = {
        'A': ['L1', 'L2'],
        'B': ['L3', 'L4'],
        'C1': ['C2', 'L1', 'L2', 'L3', 'L4'],
        'C2': ['C1', 'L1', 'L2', 'L3', 'L4'],
        'L1': ['A', 'C1', 'C2'],
        'L2': ['A', 'C1', 'C2'],
        'L3': ['B', 'C1', 'C2'],
        'L4': ['B', 'C1', 'C2']
    }
    org_ce = EventOrganizer(graph_ce)
    print(f"Exact Max (Optimal): {org_ce.find_max_invitations_exact()}")
    print(f"Greedy Result (Suboptimal): {org_ce.find_max_invitations_greedy()}")

if __name__ == "__main__":
    run_tests()