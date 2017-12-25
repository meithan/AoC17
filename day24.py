import sys
from queue import Queue

# ==========================================

# A breadth-first search to get all bridges from the given starting node
def build_bridges(components, start):

  paths = []
  open_set = Queue()
  port = start[1] if start[0] == 0 else start[0]
  open_set.put(([start], start, port))
  paths.append([start])

  while not open_set.empty():
    path, node, port = open_set.get()
    for child in components[port]:
      if child not in path:
        child_port = child[1] if child[0] == port else child[0]
        new_path = path + [child]
        open_set.put((new_path, child, child_port))
        paths.append(new_path)

  return paths

# Computes the strength of a bridge
def calc_strength(bridge):
  strength = 0
  for component in bridge:
    strength += component[0] + component[1]
  return strength

# ==========================================

# Read components from input and store them in a dict indexed by
# their ports
components = {}
with open(sys.argv[1]) as f:
  for line in f:
    component = tuple(map(int, line.strip().split("/")))
    port1 = component[0]
    port2 = component[1]
    if port1 not in components:
      components[port1] = set()
    if port2 not in components:
      components[port2] = set()
    components[port1].add(component)
    components[port2].add(component)

# foo = []
# for key in components.keys():
#   print(key, components[key])
#   foo.append(len(components[key]))
# print(sum(foo)/float(len(foo)))

max_strength = None
strongest = None
max_length = None
longest_bridges = []
for start_comp in components[0]:

  # Obtain bridges
  print("Start:",start_comp)
  bridges = build_bridges(components, start_comp)
  print("%i bridges built" % len(bridges))

  for bridge in bridges:

    # Max bridge strength
    strength = calc_strength(bridge)
    if max_strength is None or strength > max_strength:
      max_strength = strength
      strongest = bridge

    # Max length bridge(s)
    if max_length is None:
      max_length = len(bridge)
    if len(bridge) == max_length:
      longest_bridges.append(bridge)
      max_length = len(bridge)
    elif len(bridge) > max_length:
      longest_bridges = [bridge]
      max_length = len(bridge)

print("Max strength of any bridge:", max_strength)
solA = max_strength

print("%i bridges have the max length of %i" % (len(longest_bridges), max_length))
max_strength_longest = max((calc_strength(bridge) for bridge in longest_bridges))
print("Max strength of longest bridge:", max_strength_longest)
solB = max_strength_longest

print("Part A:", solA)
print("Part B:", solB)
