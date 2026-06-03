import os
from graphviz import Digraph
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ================= 1. AVL 树节点定义与操作 =================
class Node:
    def __init__(self, v):
        self.val = v
        self.left = None
        self.right = None
        self.h = 1

def h(n): return n.h if n else 0
def upd(n):
    if n: n.h = 1 + max(h(n.left), h(n.right))
def bf(n): return h(n.left) - h(n.right) if n else 0

def ins(root, v):
    if not root: return Node(v)
    if v < root.val: root.left = ins(root.left, v)
    else: root.right = ins(root.right, v)
    upd(root)
    return root

# ================= 2. 画图函数（返回图像文件路径） =================
def draw_step(root, step_num, seq):
    dot = Digraph(comment=f'Step {step_num}: Insert {seq}')
    
    def dfs(n):
        if n:
            # 节点标签：值 + 高度 + 平衡因子
            dot.node(str(n.val), f"{n.val}\nh={n.h}\nbf={bf(n)}")
            if n.left:
                dot.edge(str(n.val), str(n.left.val))
                dfs(n.left)
            if n.right:
                dot.edge(str(n.val), str(n.right.val))
                dfs(n.right)
    
    dfs(root)
    
    # 保存为 PNG 文件
    filename = f"step_{step_num}.png"
    dot.render(filename, cleanup=True, format='png')
    return filename

# ================= 3. 合并图片为 PDF =================
def merge_images_to_pdf(image_files, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    
    for img_file in image_files:
        if not os.path.exists(img_file):
            continue
        
        # 读取图片
        img = ImageReader(img_file)
        img_width, img_height = img.getSize()
        
        # 计算缩放比例，让图片适应页面
        scale = min(width / img_width, height / img_height) * 0.9  # 留点边距
        new_width = img_width * scale
        new_height = img_height * scale
        
        # 居中放置
        x = (width - new_width) / 2
        y = (height - new_height) / 2
        
        # 绘制图片
        c.drawImage(img_file, x, y, width=new_width, height=new_height)
        c.showPage()  # 新建一页
    
    c.save()

# ================= 4. 主程序：依次插入并生成 PDF =================
if __name__ == "__main__":
    seq = [30, 20, 10, 25, 40, 35, 50]
    root = None
    image_files = []
    
    for i, val in enumerate(seq, 1):
        root = ins(root, val)
        img_file = draw_step(root, i, val)
        image_files.append(img_file)
        print(f"✅ 第 {i} 步插入 {val} 完成，已保存为 {img_file}")
    
    # 合并为 PDF
    output_pdf = "avl_steps.pdf"
    merge_images_to_pdf(image_files, output_pdf)
    print(f"\n🎉 所有步骤已完成！PDF 已生成：{output_pdf}")
    
    # 清理临时图片（可选）
    # for f in image_files: os.remove(f)