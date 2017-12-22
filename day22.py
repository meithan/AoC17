from collections import defaultdict
import sys

# ==========================================

class Carrier:

  def __init__(self, nodes, part, verbose=True):
    self.x = 0
    self.y = 0
    self.direction = UP
    self.bursts = 0
    self.infections = 0
    self.nodes = nodes.copy()
    self.part = part
    self.verbose = verbose

  def step(self):

    # Get node status
    node = (self.x, self.y)
    node_status = self.nodes[node]
    if self.verbose: print("\nNode (%i,%i) is %s" % (self.x, self.y, node_status))

    # Do actions depending on node status:
    # Possibly change directions and change node status
    if node_status == "infected":
      self.turn("right")
      if self.part == "A":
        self.nodes[node] = "clean"
        if self.verbose: print("Cleaned (%i,%i)" % (self.x,self.y))
      elif self.part == "B":
        self.nodes[node] = "flagged"
        if self.verbose: print("Flagged (%i,%i)" % (self.x,self.y))

    elif node_status == "clean":
      self.turn("left")
      if self.part == "A":
        self.nodes[node] = "infected"
        self.infections += 1
        if self.verbose: print("Infected (%i,%i)" % (self.x,self.y))
      elif self.part == "B":
        self.nodes[node] = "weakened"
        if self.verbose: print("Weakened (%i,%i)" % (self.x,self.y))

    elif node_status == "weakened":
      self.nodes[node] = "infected"
      self.infections += 1
      if self.verbose: print("Infected (%i,%i)" % (self.x,self.y))

    elif node_status == "flagged":
      self.reverse()
      self.nodes[node] = "clean"
      if self.verbose: print("Cleaned (%i,%i)" % (self.x,self.y))

    # Move in the now-current direction
    if self.verbose: print("New direction: %s" % directions_names[self.direction])
    self.move()
    if self.verbose: print("Moved to (%i,%i)" % (self.x, self.y))

    self.bursts += 1

  # Move in the carrier's current direction
  def move(self):
    if self.direction == UP:
      self.y += 1
    elif self.direction == DOWN:
      self.y -= 1
    elif self.direction == RIGHT:
      self.x += 1
    elif self.direction == LEFT:
      self.x -= 1

  # Turn either "left" or "right"
  def turn(self, direc):
    if direc == "right":
      self.direction = (self.direction + 1) % 4
    elif direc == "left":
      self.direction = (self.direction - 1) % 4

  # Reverse the carrier's current direction
  def reverse(self):
    self.direction = (self.direction + 2) % 4

# ==========================================

UP = 0; RIGHT = 1; DOWN = 2; LEFT = 3
directions_names = ["up", "right", "down", "left"]

# Load initial grid from file
size = None
nodes = defaultdict(lambda: "clean")
count = 0
with open(sys.argv[1]) as f:
  for line in f:

    tokens = line.strip()

    if size is None:
      size = len(tokens)
      assert size % 2 == 1
      col = (size-1)//2

    for i in range(len(tokens)):
      row = -((size-1)//2) + i
      if tokens[i] == "#":
        nodes[(row,col)] = "infected"
        count += 1
      elif tokens[i] == ".":
        nodes[(row,col)] = "clean"

    col -= 1

print("%i x %i grid loaded" % (size, size))
print("%i initially infected nodes" % (count))

# Part A

carrier = Carrier(nodes, part="A", verbose=False)
for i in range(10000):
  carrier.step()
solA = carrier.infections

print("Part A:", solA)

# Part A

carrier = Carrier(nodes, part="B", verbose=False)
for i in range(10000000):
  carrier.step()
solB = carrier.infections

print("Part B:", solB)
