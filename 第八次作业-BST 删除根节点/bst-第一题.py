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

dot = Digraph("Original_BST")
add_nodes(dot, root)
dot.render("bst_original", view=True)