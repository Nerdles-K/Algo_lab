from collections import Counter

class UserNode:
    def __init__(self, user_id, name, friends=None):
        self.user_id = user_id
        self.name = name
        self.friends = friends if friends is not None else []
        self.left = None
        self.right = None

class UserBST:
    def __init__(self):
        self.root = None

    def insert(self, user_id, name, friends_list):
        if self.root is None:
            self.root = UserNode(user_id, name, friends_list)
        else:
            self._insert_recursive(self.root, user_id, name, friends_list)

    def _insert_recursive(self, node, user_id, name, friends_list):
        if user_id < node.user_id:
            if node.left is None:
                node.left = UserNode(user_id, name, friends_list)
            else:
                self._insert_recursive(node.left, user_id, name, friends_list)
        elif user_id > node.user_id:
            if node.right is None:
                node.right = UserNode(user_id, name, friends_list)
            else:
                self._insert_recursive(node.right, user_id, name, friends_list)
        else:
            node.name = name
            node.friends = friends_list

    def find(self, user_id):
        return self._find_recursive(self.root, user_id)

    def _find_recursive(self, node, user_id):
        if node is None or node.user_id == user_id:
            return node
        if user_id < node.user_id:
            return self._find_recursive(node.left, user_id)
        return self._find_recursive(node.right, user_id)

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.user_id)
            self._inorder_recursive(node.right, result)

    def delete(self, user_id):
        self.root = self._delete_recursive(self.root, user_id)

    def _delete_recursive(self, node, user_id):
        if node is None:
            return node

        if user_id < node.user_id:
            node.left = self._delete_recursive(node.left, user_id)
        elif user_id > node.user_id:
            node.right = self._delete_recursive(node.right, user_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._get_min_node(node.right)
            node.user_id = temp.user_id
            node.name = temp.name
            node.friends = temp.friends
            node.right = self._delete_recursive(node.right, temp.user_id)
        return node

    def _get_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def suggest_friends(self, user_id, max_suggestions=5):
        target_user = self.find(user_id)
        if target_user is None:
            return []

        target_friends_set = set(target_user.friends)
        fof_counter = Counter()

        for friend_id in target_user.friends:
            friend_node = self.find(friend_id)
            if friend_node:
                for fof_id in friend_node.friends:
                    if fof_id != user_id and fof_id not in target_friends_set:
                        fof_counter[fof_id] += 1

        return [fof_id for fof_id, count in fof_counter.most_common(max_suggestions)]


    def get_height(self):
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        if node is None:
            return -1
        return 1 + max(self._get_height_recursive(node.left), self._get_height_recursive(node.right))

    def is_balanced(self):
        return self._check_balance(self.root) != -2

    def _check_balance(self, node):
        if node is None:
            return -1
        
        left_h = self._check_balance(node.left)
        if left_h == -2: return -2
        
        right_h = self._check_balance(node.right)
        if right_h == -2: return -2

        if abs(left_h - right_h) > 1:
            return -2 # Not balanced
            
        return 1 + max(left_h, right_h)

    def get_leaf_count(self):
        return self._get_leaf_count_recursive(self.root)

    def _get_leaf_count_recursive(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return self._get_leaf_count_recursive(node.left) + self._get_leaf_count_recursive(node.right)
    

def run_edge_tests():
    print("--- Initialize UserBST ---")
    bst = UserBST()
    
    bst.insert(10, "Alice", [20, 30])
    bst.insert(5, "Bob", [10, 40])
    bst.insert(20, "Charlie", [10, 30, 50])
    bst.insert(30, "Dave", [10, 20, 50])
    bst.insert(40, "Eve", [5])
    bst.insert(50, "Frank", [20, 30])
    
    print(f"Expected In-order traversal: [5, 10, 20, 30, 40, 50]")
    print(f"Actual In-order traversal: {bst.inorder_traversal()}")
    
    print(f"\nExpected Tree height: 4")
    print(f"Actual Tree height: {bst.get_height()}")
    
    print(f"\nExpected Is balanced: False")
    print(f"Actual Is balanced: {bst.is_balanced()}")
    
    print(f"\nExpected Leaf count: 2")
    print(f"Actual Leaf count: {bst.get_leaf_count()}")

    print("\n--- Friend suggestion tests ---")
    # Alice(10)'s friends are 20, 30. Friends of 20 have 50, friends of 30 have 50. So recommend 50
    print(f"Expected Friend suggestions for Alice(10): [50]")
    print(f"Actual Friend suggestions for Alice(10): {bst.suggest_friends(10)}")
    
    # 3. Edge case: Delete non-existent user
    print("\n--- Boundary case: Delete non-existent user ---")
    bst.delete(999) 
    print(f"Expected After attempting to delete 999, tree is still intact: [5, 10, 20, 30, 40, 50]")
    print(f"Actual After attempting to delete 999: {bst.inorder_traversal()}")
    
    # 4. Edge case: Suggest friends for non-existent user
    print("\n--- Boundary case: Suggest friends for non-existent user ---")
    print(f"Expected Friend suggestions for user 999: []")
    print(f"Actual Friend suggestions for user 999: {bst.suggest_friends(999)}")
    
    # 5. Edge case: Island user (no friends)
    print("\n--- Boundary case: Island user ---")
    bst.insert(60, "Ghost", [])
    print(f"Expected Friend suggestions for Ghost(60): []")
    print(f"Actual Friend suggestions for Ghost(60): {bst.suggest_friends(60)}")
    
    # 6. Edge case: Degenerate Chain (Inserting in ascending order)
    print("\n--- Boundary case: Degenerate Chain (Inserting in ascending order) ---")
    degenerate_bst = UserBST()
    for i in range(1, 11):
        degenerate_bst.insert(i, f"User{i}", [])
    
    print(f"Expected Degenerate tree in-order traversal: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")
    print(f"Actual Degenerate tree in-order traversal: {degenerate_bst.inorder_traversal()}")
    
    print(f"\nExpected Degenerate tree height: 9 (for 10 nodes in a chain)")
    print(f"Actual Degenerate tree height: {degenerate_bst.get_height()}")
    
    print(f"\nExpected Degenerate tree is balanced: False")
    print(f"Actual Degenerate tree is balanced: {degenerate_bst.is_balanced()}")
    
    # 7. Edge case: Delete root node (ID 10)
    print("\n--- Boundary case: Delete root node (ID 10) ---")
    bst.delete(10)
    print(f"Expected In-order traversal after deleting root: [5, 20, 30, 40, 50, 60]")
    print(f"Actual In-order traversal after deleting root: {bst.inorder_traversal()}")

if __name__ == "__main__":
    run_edge_tests()