class CategoryNode:
    def __init__(self, category_id, name, post_count, parent=None):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.parent = parent
        self.children = []  

 --- 2. Tree Metric Calculations ---

def calculate_height(node):
    if node is None:
        return -1
    if not node.children:
        return 0
    max_child_height = -1
    for child in node.children:
        h = calculate_height(child)
        if h > max_child_height:
            max_child_height = h
    return 1 + max_child_height

def calculate_node_height(node, target_id):
    target_node = find_category(target_id, node)
    if target_node is None:
        return -1
    return calculate_height(target_node)

def count_nodes(node):
    if node is None:
        return 0
    count = 1
    for child in node.children:
        count += count_nodes(child)
    return count

def count_leaves(node):
    if node is None:
        return 0
    if not node.children:
        return 1
    total = 0
    for child in node.children:
        total += count_leaves(child)
    return total

def is_balanced(node):
    if node is None:
        return True
    heights = []
    for child in node.children:
        heights.append(calculate_height(child))
    
    if not heights:
        return True
    
    max_h = max(heights)
    min_h = min(heights)
    if max_h - min_h > 1:
        return False
    
    for child in node.children:
        if not is_balanced(child):
            return False
    return True

 --- 3. Tree Property Verification ---

def is_full_generalized_tree(node):
    if node is None:
        return True
    if not node.children:
        return True
    if len(node.children) < 2:
        return False
    for child in node.children:
        if not is_full_generalized_tree(child):
            return False
    return True

def is_perfect_generalized_tree(node):
    if node is None:
        return True

    height = calculate_height(node)
    fan_out = len(node.children) if node.children else 0

    def check(node, current_level):
        if not node.children:
            return current_level == height
        if len(node.children) != fan_out:
            return False
        for child in node.children:
            if not check(child, current_level + 1):
                return False
        return True

    return check(node, 0)

def is_complete_generalized_tree(node):
    if node is None:
        return True
    from collections import deque
    q = deque([node])
    found_null = False

    while q:
        current = q.popleft()
        if current is None:
            found_null = True
        else:
            if found_null:
                return False
            for child in current.children:
                q.append(child)
    return True

 --- 4. Category Search and Navigation ---

def find_category(category_id, node):
    if node is None:
        return None
    if node.category_id == category_id:
        return node
    for child in node.children:
        res = find_category(category_id, child)
        if res:
            return res
    return None

def find_path_to_root(category_id, node):
    target = find_category(category_id, node)
    path = []
    current = target
    while current is not None:
        path.append(current.name)
        current = current.parent
    return path

def lowest_common_ancestor(id1, id2, node):
    if node is None:
        return None

    path1 = find_path_to_root(id1, node)
    path2 = find_path_to_root(id2, node)

    if not path1 or not path2:
        return None

    path1.reverse()
    path2.reverse()

    lca_name = None
    for a, b in zip(path1, path2):
        if a == b:
            lca_name = a
        else:
            break
    return find_category_name(lca_name, node)

def find_category_name(name, node):
    if node is None:
        return None
    if node.name == name:
        return node
    for child in node.children:
        res = find_category_name(name, child)
        if res:
            return res
    return None

 --- 5. Edge Test Suite ---

def run_edge_tests():
    print("=== Running Edge Cases Test Suite ===")

    # 1. Edge Case: Empty Tree
    print("\n--- 1. Testing Empty Tree ---")
    empty_node = None
    print(f"Height is -1: {calculate_height(empty_node) == -1}")
    print(f"Node count is 0: {count_nodes(empty_node) == 0}")
    print(f"Is balanced (True): {is_balanced(empty_node) == True}")
    print(f"Is complete (True): {is_complete_generalized_tree(empty_node) == True}")
    print(f"LCA of 1 and 2 is None: {lowest_common_ancestor(1, 2, empty_node) is None}")

    # 2. Edge Case: Single Node Tree
    print("\n--- 2. Testing Single Node Tree ---")
    single_node = CategoryNode(1, "Root_Only", 100)
    print(f"Height is 0: {calculate_height(single_node) == 0}")
    print(f"Leaf count is 1: {count_leaves(single_node) == 1}")
    print(f"Is perfect binary tree (True): {is_perfect_generalized_tree(single_node) == True}")
    print(f"Path to root: {find_path_to_root(1, single_node) == ['Root_Only']}")

    # 3. Edge Case: Completely Unbalanced Tree (Chain)
    print("\n--- 3. Testing Completely Unbalanced Tree (Left-skewed) ---")
    n1 = CategoryNode(1, "Level_0", 10)
    n2 = CategoryNode(2, "Level_1", 20, parent=n1)
    n1.children.append(n2)
    n3 = CategoryNode(3, "Level_2", 30, parent=n2)
    n2.children.append(n3)

    print(f"Height is 2: {calculate_height(n1) == 2}")
    print(f"Is balanced (False): {is_balanced(n1) == False}")
    print(f"Is full generalized tree (False): {is_full_generalized_tree(n1) == False}")
    print(f"Path from leaf to root: {find_path_to_root(3, n1) == ['Level_2', 'Level_1', 'Level_0']}")

    # 4. Edge Case: Non-existent Node Searches
    print("\n--- 4. Testing Non-existent Nodes ---")
    print(f"Find category 99 (None): {find_category(99, n1) is None}")
    print(f"Node height for 99 (-1): {calculate_node_height(n1, 99) == -1}")
    print(f"Path to root for 99 (Empty List): {find_path_to_root(99, n1) == []}")

    # 5. Edge Case: LCA (Ancestor-Descendant)
    print("\n--- 5. Testing LCA (Ancestor/Descendant Relationship) ---")
    lca_node = lowest_common_ancestor(1, 3, n1)
    print(f"LCA of 1 and 3 is Level_0: {lca_node.name == 'Level_0' if lca_node else False}")

if __name__ == "__main__":
    run_edge_tests()
