import sys

# ==========================================

class Node:
  def __init__(self, name, weight, children):
    self.name = name
    self.weight = weight
    self.children = children
    self.parent = None
    self.subtree_weight = None
    self.depth = None
  def __repr__(self):
    if self.children is None:
      childstr = "None (%i)" % self.weight
    else:
      childstr = "[" + ", ".join([x.name for x in self.children]) +  "]"
      childstr += " (%s)" % self.subtree_weight
    return "%s (%i) -> %s" % (self.name, self.weight, childstr)

# ==========================================

with open(sys.argv[1]) as f:
  lines = f.readlines()

names = {}
tree = []

# Create nodes
for line in lines:
  if "->" in line:
    nodeweight, children = line.strip().split(" -> ")
    children = children.split(", ")
  else:
    nodeweight = line.strip()
    children = None
  name, weight = nodeweight.split()
  weight = int(weight.strip("(").strip(")"))
  #print(name, weight, children)
  node = Node(name, weight, children)
  tree.append(node)
  names[name] = node

# Determine parents and convert children nodes into objects
for node in tree:
  if node.children is not None:
    for i,child_name in enumerate(node.children):
      node.children[i] = names[child_name]
      node.children[i].parent = node

# Part A

# Pick any leaf and follow it up to the root
for node in tree:
  if node.children is None:
    while node.parent is not None:
      #print(node.name, node.parent)
      node = node.parent
    root = node
    break
solA = root.name

# Part B

# Compute node depths
root.depth = 0
nodes = root.children
while len(nodes) != 0:
  child = nodes.pop()
  child.depth = child.parent.depth + 1
  if child.children is not None:
    nodes = child.children + nodes

# First, recursively determine weight of subtrees ...
def get_subtree_weight(root_node):
  if root_node.children is None:
    root_node.subtree_weight = root_node.weight
    return root_node.weight
  else:
    w = 0
    for child in root_node.children:
      if child.subtree_weight is None:
        get_subtree_weight(child)
      w += child.subtree_weight
    root_node.subtree_weight = root_node.weight + w
    return root_node.subtree_weight
root.subtree_weight = get_subtree_weight(root)

# ... then determine which one is out of balance
solB = None
depth = None
for node in tree:
  if node.children is not None:
    ws = [x.subtree_weight for x in node.children]
    if len(ws) == 1: continue
    for k,child in enumerate(node.children):
      if ws.count(child.subtree_weight) == 1:
        bad_node = child
        kn = (k+1) % len(node.children)
        good_weight = node.children[kn].subtree_weight
        corrected = bad_node.weight + (good_weight - bad_node.subtree_weight)
        if depth is None or bad_node.depth > depth:
          solB = corrected
          depth = bad_node.depth

print(solA)
print(solB)
