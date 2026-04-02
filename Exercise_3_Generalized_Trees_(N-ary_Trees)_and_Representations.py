class GeneralizedCategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id 
        self.name = name            
        self.post_count = post_count   
        self.children = []             
        self.parent = None             

# 2. 定义 【二叉树节点】（转换要用）
class BinaryCategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.left = None   
        self.right = None  

# ======================================================
# Part A：二叉树 → 多叉树
# ======================================================
def binary_to_generalized(binary_node):
    if not binary_node:
        return None

    gen_node = GeneralizedCategoryNode(
        binary_node.category_id,
        binary_node.name,
        binary_node.post_count
    )

    child = binary_node.left
    while child:
        gen_child = binary_to_generalized(child)
        gen_node.children.append(gen_child)
        gen_child.parent = gen_node
        child = child.right

    return gen_node

# ======================================================
# Part B：多叉树 → 二叉树（左孩子右兄弟）
# ======================================================
def generalized_to_binary(gen_node):
    if not gen_node:
        return None

    binary_node = BinaryCategoryNode(
        gen_node.category_id,
        gen_node.name,
        gen_node.post_count
    )

    if not gen_node.children:
        return binary_node

    binary_node.left = generalized_to_binary(gen_node.children[0])
    sibling = binary_node.left
    for i in range(1, len(gen_node.children)):
        sibling.right = generalized_to_binary(gen_node.children[i])
        sibling = sibling.right

    return binary_node

# ======================================================
# 多叉树遍历（前序、后序、层序）
# ======================================================

# 前序遍历：根 → 孩子们
def pre_order_generalized(node):
    if not node:
        return []
    res = [node.name]
    for child in node.children:
        res += pre_order_generalized(child)
    return res

# 后序遍历：孩子们 → 根
def post_order_generalized(node):
    if not node:
        return []
    res = []
    for child in node.children:
        res += post_order_generalized(child)
    res.append(node.name)
    return res

# 层序遍历（一层一层）
def level_order_generalized(node):
    if not node:
        return []
    from collections import deque
    q = deque([node])
    res = []
    while q:
        cur = q.popleft()
        res.append(cur.name)
        for child in cur.children:
            q.append(child)
    return res

# ======================================================
# 多叉树 计算（高度、节点数、叶子数、扇出、分支因子）
# ======================================================

# 树高度
def calculate_height_generalized(node):
    if not node:
        return -1
    if not node.children:
        return 0
    max_h = -1
    for child in node.children:
        max_h = max(max_h, calculate_height_generalized(child))
    return 1 + max_h

# 总节点数
def count_nodes_generalized(node):
    if not node:
        return 0
    count = 1
    for child in node.children:
        count += count_nodes_generalized(child)
    return count

# 叶子数（没有孩子）
def count_leaves_generalized(node):
    if not node:
        return 0
    if not node.children:
        return 1
    total = 0
    for child in node.children:
        total += count_leaves_generalized(child)
    return total

# 最大扇出（一个节点最多有几个孩子）
def calculate_fan_out(node):
    if not node:
        return 0
    max_fan = len(node.children)
    for child in node.children:
        max_fan = max(max_fan, calculate_fan_out(child))
    return max_fan

# 平均分支因子（非叶子节点平均有几个孩子）
def calculate_branching_factor(node):
    total_children = 0
    non_leaf = 0

    def dfs(n):
        nonlocal total_children, non_leaf
        if not n:
            return
        if n.children:
            non_leaf += 1
            total_children += len(n.children)
        for c in n.children:
            dfs(c)

    dfs(node)
    if non_leaf == 0:
        return 0.0
    return total_children / non_leaf
    # 3. 二叉 → 多叉
    gen_root = binary_to_generalized(binary_root)
    print("二叉树转回多叉树成功！")
    print("转回后前序遍历:", pre_order_generalized(gen_root))
