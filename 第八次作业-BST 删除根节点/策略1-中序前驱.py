from graphviz import Digraph

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def find_predecessor(root):
    cur = root.left
    while cur and cur.right:
        cur = cur.right
    return cur

def delete_predecessor(root, key):
    if root is None:
        return None

    if key < root.val:
        root.left = delete_predecessor(root.left, key)
    elif key > root.val:
        root.right = delete_predecessor(root.right, key)
    else:
        # 叶子 / 单子节点
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left

        # 两个子节点 → 中序前驱
        pred = find_predecessor(root)
        root.val = pred.val
        root.left = delete_predecessor(root.left, pred.val)

    return root

def add_nodes(graph, node):
    if node:
        graph.node(str(node.val), str(node.val))
        if node.left:
            graph.edge(str(node.val), str(node.left.val))
            add_nodes(graph, node.left)
        if node.right:
            graph.edge(str(node.val), str(node.right.val))
            add_nodes(graph, node.right)

# ===== 主程序 =====
seq = [50, 30, 70, 20, 40, 60, 80]

root = None
for x in seq:
    root = insert(root, x)

root = delete_predecessor(root, 50)

dot = Digraph("BST_Delete_Predecessor")
add_nodes(dot, root)
dot.render("bst_delete_predecessor", view=True)