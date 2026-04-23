from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}  # key: char, value: TrieNode
        self.is_end_of_username = False
        self.user_id = None

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, username, user_id):
        current = self.root
        for char in username.lower():
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_username = True
        current.user_id = user_id

    def search(self, username):
        current = self.root
        for char in username.lower():
            if char not in current.children:
                return None
            current = current.children[char]
        return current.user_id if current.is_end_of_username else None

    def starts_with(self, prefix):
        current = self.root
        for char in prefix.lower():
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def autocomplete(self, prefix, max_results=10):
        current = self.root
        result = []
        
        for char in prefix.lower():
            if char not in current.children:
                return []
            current = current.children[char]
        
        q = deque()
        q.append((current, prefix.lower()))
        
        while q and len(result) < max_results:
            node, word = q.popleft()
            if node.is_end_of_username:
                result.append((word, node.user_id))
            for char in sorted(node.children.keys()):
                q.append((node.children[char], word + char))
        
        return result

    def count_words(self):
        return self._count_words_recursive(self.root)

    def _count_words_recursive(self, node):
        count = 0
        if node.is_end_of_username:
            count += 1
        for child in node.children.values():
            count += self._count_words_recursive(child)
        return count

    def get_height(self):
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        if not node.children:
            return 0
        max_child_height = 0
        for child in node.children.values():
            max_child_height = max(max_child_height, self._get_height_recursive(child))
        return 1 + max_child_height

    def get_total_nodes(self):
        return self._get_total_nodes_recursive(self.root)

    def _get_total_nodes_recursive(self, node):
        count = 1
        for child in node.children.values():
            count += self._get_total_nodes_recursive(child)
        return count

    def delete(self, username):
        self._delete_recursive(self.root, username.lower(), 0)

    def _delete_recursive(self, node, word, index):
        if index == len(word):
            if not node.is_end_of_username:
                return False
            node.is_end_of_username = False
            node.user_id = None
            return len(node.children) == 0

        char = word[index]
        if char not in node.children:
            return False

        can_delete_child = self._delete_recursive(node.children[char], word, index + 1)
        if can_delete_child:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_username

        return False


def run_trie_edge_tests():
    print("--- Initialize AutocompleteTrie ---")
    trie = AutocompleteTrie()

    trie.insert("alice", 101)
    trie.insert("alice123", 102)
    trie.insert("bob", 201)
    trie.insert("bobsmith", 202)
    trie.insert("charlie", 301)
    trie.insert("dave", 401)

    print("=== Basic Insert & Search ===")
    print(f"Search 'alice' → Expected:101, Actual:{trie.search('alice')}")
    print(f"Search 'bob' → Expected:201, Actual:{trie.search('bob')}")
    print(f"Search 'none' → Expected:None, Actual:{trie.search('none')}")

    print("\n=== starts_with ===")
    print(f"starts_with 'ali' → Expected:True, Actual:{trie.starts_with('ali')}")
    print(f"starts_with 'bo' → Expected:True, Actual:{trie.starts_with('bo')}")
    print(f"starts_with 'xyz' → Expected:False, Actual:{trie.starts_with('xyz')}")

    print("\n=== Autocomplete ===")
    print("Prefix 'ali' →", trie.autocomplete("ali"))
    print("Prefix 'bob' →", trie.autocomplete("bob"))
    print("Prefix 'x' →", trie.autocomplete("x"))
    print("Prefix 'a' max 1 →", trie.autocomplete("a", max_results=1))

    print("\n=== Trie Analytics ===")
    print(f"Total usernames: {trie.count_words()}")
    print(f"Trie height (longest username): {trie.get_height()}")
    print(f"Total nodes: {trie.get_total_nodes()}")

    print("\n=== Delete Tests ===")
    trie.delete("alice")
    print(f"After delete 'alice', search → Expected:None, Actual:{trie.search('alice')}")
    print(f"Autocomplete 'ali' still has alice123 →", trie.autocomplete("ali"))

    trie.delete("nonexist")
    print("Delete non-existent username → no error, tree intact")

    print("\n=== Edge Cases ===")
    print("Autocomplete empty prefix →", trie.autocomplete(""))
    trie.insert("", 999)
    print("Insert empty username, search →", trie.search(""))
    trie.delete("")

if __name__ == "__main__":
    run_trie_edge_tests()
