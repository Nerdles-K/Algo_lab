class CategoryNode:
    """Category Node structure representing social media content categories."""
    def __init__(self, category_id, name, post_count, parent=None):
        self.category_id = category_id  
        self.name = name                
        self.post_count = post_count    
        self.left = None                
        self.right = None               
        self.parent = parent            

# --- 2. Tree Metric Calculations ---

def calculate_height(node):
    if node is None:
        return -1
    return 1 + max(calculate_height(node.left), calculate_height(node.right))

def calculate_node_height(node, target_id):
    target_node = find_category(target_id, node)
    if target_node is None:
        return -1
    return calculate_height(target_node)

def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

def count_leaves(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)

def is_balanced(node):
    if node is None:
        return True
    left_h = calculate_height(node.left)
    right_h = calculate_height(node.right)
    if abs(left_h - right_h) > 1:
        return False
    return is_balanced(node.left) and is_balanced(node.right)

# --- 3. Tree Property Verification ---

def is_full_binary_tree(node):
    if node is None:
        return True
    if node.left is None and node.right is None:
        return True
    if node.left is not None and node.right is not None:
        return is_full_binary_tree(node.left) and is_full_binary_tree(node.right)
    return False

def is_perfect_binary_tree(node):
    if node is None:
        return True
    h = calculate_height(node)
    n = count_nodes(node)
    return n == (2 ** (h + 1)) - 1

def is_complete_binary_tree(node):
    if node is None:
        return True
    queue = [node]
    flag = False
    
    while queue:
        current = queue.pop(0)
        if current is None:
            flag = True
        else:
            if flag:
                return False 
            queue.append(current.left)
            queue.append(current.right)
    return True

# --- 4. Category Search and Navigation ---

def find_category(category_id, node):
    if node is None:
        return None
    if node.category_id == category_id:
        return node
    
    left_result = find_category(category_id, node.left)
    if left_result is not None:
        return left_result
        
    return find_category(category_id, node.right)

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
    if node.category_id == id1 or node.category_id == id2:
        return node
        
    left_lca = lowest_common_ancestor(id1, id2, node.left)
    right_lca = lowest_common_ancestor(id1, id2, node.right)
    
    if left_lca is not None and right_lca is not None:
        return node 
        
    return left_lca if left_lca is not None else right_lca

def run_edge_tests():
    print("=== Running Edge Cases Test Suite ===")
    
    # 1. Edge Case: Empty Tree
    print("\n--- 1. Testing Empty Tree ---")
    empty_node = None
    print(f"Height is -1: {calculate_height(empty_node) == -1}")
    print(f"Node count is 0: {count_nodes(empty_node) == 0}")
    print(f"Is balanced (True): {is_balanced(empty_node) == True}")
    print(f"Is complete (True): {is_complete_binary_tree(empty_node) == True}")
    print(f"LCA of 1 and 2 is None: {lowest_common_ancestor(1, 2, empty_node) is None}")

    # 2. Edge Case: Single Node Tree
    print("\n--- 2. Testing Single Node Tree ---")
    single_node = CategoryNode(1, "Root_Only", 100)
    print(f"Height is 0: {calculate_height(single_node) == 0}")
    print(f"Leaf count is 1: {count_leaves(single_node) == 1}")
    print(f"Is perfect binary tree (True): {is_perfect_binary_tree(single_node) == True}")
    print(f"Path to root: {find_path_to_root(1, single_node) == ['Root_Only']}")

    # 3. Edge Case: Completely Unbalanced Tree (Left-skewed / Linked List)
    print("\n--- 3. Testing Completely Unbalanced Tree (Left-skewed) ---")
    n1 = CategoryNode(1, "Level_0", 10)
    n2 = CategoryNode(2, "Level_1", 20, parent=n1)
    n1.left = n2
    n3 = CategoryNode(3, "Level_2", 30, parent=n2)
    n2.left = n3
    
    print(f"Height is 2: {calculate_height(n1) == 2}")
    print(f"Is balanced (False): {is_balanced(n1) == False}")
    print(f"Is full binary tree (False): {is_full_binary_tree(n1) == False}")
    print(f"Path from leaf to root: {find_path_to_root(3, n1) == ['Level_2', 'Level_1', 'Level_0']}")

    # 4. Edge Case: Non-existent Node Searches
    print("\n--- 4. Testing Non-existent Nodes ---")
    print(f"Find category 99 (None): {find_category(99, n1) is None}")
    print(f"Node height for 99 (-1): {calculate_node_height(n1, 99) == -1}")
    print(f"Path to root for 99 (Empty List): {find_path_to_root(99, n1) == []}")

    # 5. Edge Case: LCA where one node is ancestor of the other
    print("\n--- 5. Testing LCA (Ancestor/Descendant Relationship) ---")
    # In the skewed tree (n1 -> n2 -> n3), LCA of n1 and n3 should be n1
    lca_node = lowest_common_ancestor(1, 3, n1)
    print(f"LCA of 1 and 3 is Level_0: {lca_node.name == 'Level_0' if lca_node else False}")

if __name__ == "__main__":
    run_edge_tests()