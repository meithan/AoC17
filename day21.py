import re
import sys

# ==========================================

# Rotates the rule clockwise once
def rotate(rule):
  if len(rule) == 2*2:
    return rule[2] + rule[0] + \
           rule[3] + rule[1]
  elif len(rule) == 3*3:
    return rule[6] + rule[3] + rule[0] + \
           rule[7] + rule[4] + rule[1] + \
           rule[8] + rule[5] + rule[2]


# Flips the rule horizontally
def flip(rule):
  if len(rule) == 2*2:
    return rule[1] + rule[0] + \
           rule[3] + rule[2]
  elif len(rule) == 3*3:
    return rule[2] + rule[1] + rule[0] + \
           rule[5] + rule[4] + rule[3] + \
           rule[8] + rule[7] + rule[6]


# Integer square root
# (i.e. greatest integer x such that x*x <= n)
def isqrt(n):
  x = n
  y = (x + 1) // 2
  while y < x:
    x = y
    y = (x + n // x) // 2
  return x


# Extracts the subgrids
def split_subgrids(grid):

  size = isqrt(len(grid))
  subgrids = []

  if size % 2 == 0:
    div = size // 2
    for j in range(div):
      for i in range(div):
        k0 = 2*size*j + 2*i
        subgrid = grid[k0] + grid[k0+1] + \
                  grid[k0+size] + grid[k0+size+1]
        subgrids.append(subgrid)

  elif size % 3 == 0:
    div = size // 3
    for j in range(div):
      for i in range(div):
        k0 = 3*size*j + 3*i
        subgrid = grid[k0] + grid[k0+1] + grid[k0+2] + \
                  grid[k0+size] + grid[k0+size+1] + grid[k0+size+2] + \
                  grid[k0+2*size] + grid[k0+2*size+1] + grid[k0+2*size+2]
        subgrids.append(subgrid)

  return subgrids


# Joins the array of subgrids into a new grid
def join_subgrids(subgrids):

  subsize = isqrt(len(subgrids[0]))
  subslen = isqrt(len(subgrids))

  new_grid = ""
  for sj in range(subslen):
    for k in range(subsize):
      for si in range(subslen):
        new_grid += subgrids[sj*subslen + si][k*subsize:k*subsize+subsize]

  return(new_grid)


# Applies a single iteration of the enhancement algorithm
def enhance(grid):

  # Split the grid into subgrids
  subgrids = split_subgrids(grid)

  # Substitute the subgrids using the rules
  for i in range(len(subgrids)):
    subgrids[i] = rules[subgrids[i]]

  # Join new subgrids
  new_grid = join_subgrids(subgrids)

  return new_grid


def print_grid(grid):

  size = isqrt(len(grid))
  for i in range(size):
    print(grid[size*i:size*(i+1)])

# ==========================================

# Load rules from file
rules = {}
with open(sys.argv[1]) as f:
  for line in f:
    regex = '(.*) => (.*)'
    m = re.search(regex, line.strip())
    rules[m.group(1).replace("/","")] = m.group(2).replace("/","")
print("%i rules loaded from input" % len(rules))
#print(rules)

# Add rotated/flipped versions of each rule (if different)
for rule in list(rules.keys()):
  if flip(rule) not in rules:
    rules[flip(rule)] = rules[rule]
  new_rule = rule
  for i in range(3):
    new_rule = rotate(new_rule)
    if new_rule not in rules:
      rules[new_rule] = rules[rule]
    if flip(new_rule) not in rules:
      rules[flip(new_rule)] = rules[rule]
print("%i rules after rotations/flips" % len(rules))
#for rule in rules: print(rule, rules[rule])

# The starting pattern
grid = ".#...####"
#print_grid(grid)

# Now iterate the algorithm
numits = 18
for it in range(1,numits+1):

  grid = enhance(grid)
  print(it)
  #print_grid(grid)

  # Part A: "on" pixles (#) after 5 iterations
  if it == 5:
    solA = grid.count("#")


# Part B: "on" pixles (#) after 18 iterations
solB = grid.count("#")


print("Part A:", solA)
print("Part B:", solB)
