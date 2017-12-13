import sys

# ==========================================

def move(x, y, direc):
  if direc == "n": return (x, y+1)
  elif direc == "s": return (x, y-1)
  elif direc == "ne": return (x+1, y+0.5)
  elif direc == "se": return (x+1, y-0.5)
  elif direc == "nw": return (x-1, y+0.5)
  elif direc == "sw": return (x-1, y-0.5)

def walk_to_origin(x0, y0):
  x = x0
  y = y0
  steps = []
  while not (x == 0 and y == 0):
    if x > 0: ew = "w"
    elif x < 0: ew = "e"
    elif x == 0: ew = ""
    if y > 0: ns = "s"
    elif y < 0: ns = "n"
    elif y == 0: ns = "n"
    direc = ns + ew
    x, y = move(x, y, direc)
    steps.append("direc")
    #print(direc,x,y)
  return steps

def dist_to_origin(x0, y0):
  return max(x0, y0 + 0.5*x0)

# ==========================================

with open(sys.argv[1]) as f:
  line = f.readline().strip()

#line = "ne,ne,ne"
#line = "ne,ne,sw,sw"
#line = "ne,ne,s,s"
#line = "se,sw,se,sw,sw"

direcs = line.split(",")
#print(len(direcs),"steps")
#print(direcs)

max_dist = None
x = 0
y = 0
for direc in direcs:
  x, y = move(x, y, direc)
  dist = dist_to_origin(x, y)
  #print("x0 = %i, y0 = %.1f, dist=%i" % (x,y,dist))
  if max_dist is None or dist > max_dist:
    max_dist = dist
  #print(x,y)

solA = int(dist)
solB = int(max_dist)
print(solA)
print(solB)
