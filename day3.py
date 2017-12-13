import sys

with open(sys.argv[1]) as f:
  square = int(f.readline())

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

print(solA)
print(solB)
