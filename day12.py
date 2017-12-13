import sys

# ==========================================

def get_components(connections):

  components = []
  visited = set()
  for progid in connections:
    if progid not in visited:

      component = set()
      to_check = [progid]
      while len(to_check) > 0:
        progid = to_check.pop()
        component.add(progid)
        visited.add(progid)
        for neighid in connections[progid]:
          if neighid not in visited:
            to_check.append(neighid)

      components.append(component)

  return components

# ==========================================

with open(sys.argv[1]) as f:
  lines = f.readlines()

connections = {}
for line in lines:
  progid, neighs = line.strip().split(" <-> ")
  connections[progid] = neighs.split(", ")

components = get_components(connections)
solB = len(components)

for comp in components:
  if '0' in comp:
    solA = len(comp)
    break

print(solA)
print(solB)
