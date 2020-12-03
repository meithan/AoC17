import sys

# ==================================

RIGHT = 0; UP = 1; LEFT = 2; DOWN = 3
directions = [RIGHT, UP, LEFT, DOWN]
direcnames = {RIGHT:"R", UP:"U", LEFT:"L", DOWN:"D"}

def move(x, y, direc):
  if direc == RIGHT:
    return x+1, y
  elif direc == UP:
    return x, y+1
  elif direc == LEFT:
    return x-1, y
  elif direc == DOWN:
    return x, y-1

def get_neighs_values(x, y, values):
  s = 0
  for dx in [-1,0,+1]:
    for dy in [-1,0,+1]:
      if not (dx == 0 and dy == 0):
        xn = x + dx; yn = y + dy
        if (xn, yn) in values:
          s += values[(xn,yn)]
  return s

# ==================================
# ALTERNATE ANALYTICAL SOLUTION FOR PART A

# Return the coords of the "origin" of layer l
def layer_origin(l):
  if l == 1:
    return (0, 0)
  else:
    return (l-1, 2-l)

# Alternate (analytical) solution for part A
# Returns the x,y coordinates of the given sequential
# number in the spiral grid
def get_coords(N):

  if N == 1: return 0

  # Determine layer number (first layer = 1)
  # The total number of squares up to layer l is (2*l-1)^2
  l = 1
  while (2*l-1)**2 < N: l += 1

  # Now get layer origin, determine offset, and determine position
  lx, ly = layer_origin(l)
  offset = N - (2*(l-1)-1)**2 - 1
  if 0 <= offset <= (2*l-1)-3:
    return lx, ly + offset
  elif (2*l-1)-2 <= offset <= 2*(2*l-1)-3:
    return lx - (offset - ((2*l-1)-2)), ly + (2*l-1) - 2
  elif 2*(2*l-1)-2 <= offset <= 3*(2*l-1)-5:
    return lx - (2*l-2), ly + (2*l-4) - (offset-(2*(2*l-1)-2))
  elif 3*(2*l-1)-4 <= offset <= 4*(2*l-1)-5:
    return lx - (2*l-2) + (offset-(3*(2*l-1)-4)), ly-1

# ==================================

with open(sys.argv[1]) as f:
  square = int(f.readline())

solB = None
x = 0
y = 0
direc = RIGHT
visited = set([(0,0)])
values = {(0,0):1}

for i in range(square-1):
  #print(x,y,direcnames[direc],"-> ",end="")
  x, y = move(x, y, direc)
  #print(x,y)
  visited.add((x,y))
  values[(x,y)] = get_neighs_values(x, y, values)
  new_direc = directions[(direc+1)%4]
  nx, ny = move(x, y, new_direc)
  if (nx, ny) not in visited:
    direc = new_direc
  if solB is None and values[(x,y)] > square:
    solB = values[(x,y)]
  #print(direcnames[new_direc],nx,ny)
#print(x,y)

solA = abs(x) + abs(y)

# Alternate solution with no iteration
xalt, yalt = get_coords(square)
solA_alt = abs(xalt) + abs(yalt)

print(solA, solA_alt)
print(solB)
