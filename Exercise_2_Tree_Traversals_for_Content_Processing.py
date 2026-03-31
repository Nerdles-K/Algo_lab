class CategoryNode:
    def __init__(self, name, post_count, left=None, right=None, parent=None):
        self.name = name
        self.post_count = post_count
        self.left = left
        self.right = right
        self.parent = parent

# Part A — In-order Traversal

def in_order_collect(node):
    if node is None:
        return []
    return in_order_collect(node.left) + [node.name] + in_order_collect(node.right)


def in_order_accumulate_posts(node):
    result = []
    running = 0

    def visit(n):
        nonlocal running
        if n is None:
            return
        visit(n.left)
        running += n.post_count
        result.append((n.name, running))
        visit(n.right)

    visit(node)
    return result


def in_order_find_kth(k, node):
    counter = 0
    found = None

    def visit(n):
        nonlocal counter, found
        if n is None or found is not None:
            return
        visit(n.left)
        counter += 1
        if counter == k:
            found = n
            return
        visit(n.right)

    visit(node)
    return found


# Part B — Pre-order Traversal

def pre_order_export(node, indent=0):
    if node is None:
        return ""
    line = "  " * indent + f"{node.name}({node.post_count})\n"
    line += pre_order_export(node.left, indent + 1)
    line += pre_order_export(node.right, indent + 1)
    return line


def pre_order_copy(node):
    if node is None:
        return None

    new_node = CategoryNode(node.name, node.post_count)

    new_node.left = pre_order_copy(node.left)
    new_node.right = pre_order_copy(node.right)

    if new_node.left:
        new_node.left.parent = new_node
    if new_node.right:
        new_node.right.parent = new_node

    return new_node


def pre_order_serialize(node):
    if node is None:
        return "none"
    left_str = pre_order_serialize(node.left)
    right_str = pre_order_serialize(node.right)
    return f"{node.name}({node.post_count})|{left_str}|{right_str}"


# Part C — Post-order Traversal

def post_order_total_posts(node):
    if node is None:
        return 0
    return (post_order_total_posts(node.left) +
            post_order_total_posts(node.right) +
            node.post_count)


def post_order_average_depth(node):
    leaf_depths = []

    def visit(n, depth):
        if n is None:
            return
        if n.left is None and n.right is None:
            leaf_depths.append(depth)
            return
        visit(n.left, depth + 1)
        visit(n.right, depth + 1)

    visit(node, 0)

    if not leaf_depths:
        return None

    return sum(leaf_depths) / len(leaf_depths)


def post_order_collect_leaves(node):
    if node is None:
        return []
    if node.left is None and node.right is None:
        return [node]
    return post_order_collect_leaves(node.left) + post_order_collect_leaves(node.right)


# Analytics Functions

def find_most_popular_category(node):
    if node is None:
        return None

    best = node

    def visit(n):
        nonlocal best
        if n is None:
            return
        if n.post_count > best.post_count:
            best = n
        visit(n.left)
        visit(n.right)

    visit(node)
    return best


def category_with_most_subcategories(node):
    if node is None:
        return None

    best = None
    best_count = -1

    def visit(n):
        nonlocal best, best_count
        if n is None:
            return

        count = 0
        if n.left:
            count += 1
        if n.right:
            count += 1

        if count > best_count:
            best_count = count
            best = n

        visit(n.left)
        visit(n.right)

    visit(node)
    return best


from collections import deque, defaultdict

def distribution_by_depth(node):
    if node is None:
        return {}

    result = defaultdict(int)
    queue = deque([(node, 0)])

    while queue:
        current, depth = queue.popleft()
        result[depth] += 1

        if current.left:
            queue.append((current.left, depth + 1))
        if current.right:
            queue.append((current.right, depth + 1))

    return dict(result)

# Edge Tests

if __name__ == "__main__":

    print("=== BASIC TESTS ===")

    # 1. Empty Tree
    empty = None
    print("\n-- Empty Tree --")
    print("in_order_collect:", in_order_collect(empty))
    print("total_posts:", post_order_total_posts(empty))

    # 2. Single Node
    single = CategoryNode("Root", 10)
    print("\n-- Single Node --")
    print("in_order_collect:", in_order_collect(single))
    print("leaves:", [n.name for n in post_order_collect_leaves(single)])

    # 3. Small Normal Tree
    B = CategoryNode("B", 5)
    C = CategoryNode("C", 7)
    A = CategoryNode("A", 10, B, C)

    print("\n-- Small Tree --")
    print("in_order_collect:", in_order_collect(A))
    print("total_posts:", post_order_total_posts(A))
    print("most_popular:", find_most_popular_category(A).name)
    print("depth_distribution:", distribution_by_depth(A))

