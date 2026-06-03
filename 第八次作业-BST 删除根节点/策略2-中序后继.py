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

def find_successor(root):
    cur = root.right
    while cur and cur.left:
        cur = cur.left
    return cur

def delete_successor(root, key):
    if root is None:
        return None

    if key < root.val:
        root.left = delete_successor(root.left, key)
    elif key > root.val:
        root.right = delete_successor(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left

        # 两个子节点 → 中序后继
        succ = find_successor(root)
        root.val = succ.val
        root.right = delete_successor(root.right, succ.val)

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

root = delete_successor(root, 50)

dot = Digraph("BST_Delete_Successor")
add_nodes(dot, root)
dot.render("bst_delete_successor", view=True)