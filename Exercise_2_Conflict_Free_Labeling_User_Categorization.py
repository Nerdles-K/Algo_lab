def is_valid_labeling(labeling, graph):
    """Verify no two adjacent nodes share the same label. O(E)"""
    for u in graph:
        for v in graph[u]:
            if labeling[u] == labeling[v]:
                return False
    return True

def is_safe(node, color, labeling, graph):
    """Check if assigning 'color' to 'node' conflicts with any neighbor."""
    for neighbor in graph[node]:
        if labeling[neighbor] == color:
            return False
    return True

def assign_labels(k, graph):
    """Try to color the graph with at most k colors via backtracking. O(k^N)"""
    n = len(graph)
    labeling = [-1] * n

    def backtrack(node):
        if node == n:
            return True
        for color in range(k):
            if is_safe(node, color, labeling, graph):
                labeling[node] = color
                if backtrack(node + 1):
                    return True
                labeling[node] = -1
        return False

    success = backtrack(0)
    return (success, labeling if success else [])

def find_min_labels(graph):
    """Find the minimum chromatic number by trying k = 1, 2, 3, ..."""
    n = len(graph)
    if n == 0:
        return (0, [])
    for k in range(1, n + 1):
        success, labeling = assign_labels(k, graph)
        if success:
            return (k, labeling)
    return (n, list(range(n)))

if __name__ == "__main__":

    print("=== Edge Case 1: Empty graph ===")
    min_k, labeling = find_min_labels({})
    print(f"  Min labels: {min_k} → expected 0")

    print("\n=== Edge Case 2: Fully connected K3 ===")
    graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    min_k, labeling = find_min_labels(graph)
    print(f"  Min labels: {min_k} → expected 3")
    print(f"  Valid?    : {is_valid_labeling(labeling, graph)}")

    print("\n=== Edge Case 3: assign_labels(1) with edges ===")
    success, _ = assign_labels(1, {0: [1], 1: [0]})
    print(f"  Success: {success} → expected False")

    print("\n=== Edge Case 4: Disconnected nodes ===")
    graph = {0: [], 1: [], 2: []}
    min_k, labeling = find_min_labels(graph)
    print(f"  Min labels: {min_k} → expected 1")
    print(f"  Valid?    : {is_valid_labeling(labeling, graph)}")