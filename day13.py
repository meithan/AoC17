import sys
from functools import reduce

# ==========================================

def get_scanner_pos(rnge, time):


  period = 2*rnge - 2
  k = time % period
  if k > (rnge-1):
    k = period - k
  return k

def traverse(layers, delay, stop=False):

  caught_layers = []
  for depth in layers:
    time = delay + depth
    scanpos = get_scanner_pos(layers[depth], time)
    if scanpos == 0:
      caught_layers.append((depth, layers[depth]))
      if stop:
        return caught_layers

  return caught_layers

# ==========================================

layers = {}
with open(sys.argv[1]) as f:
  for line in f:
    tokens = line.strip().split(": ")
    layers[int(tokens[0])] = int(tokens[1])

#for time in range(12):
#  print(time, get_scanner_depth(3,time))

# Part A
caught_layers = traverse(layers, 0)
solA = reduce(lambda x,y: x + y[0]*y[1], caught_layers, 0)

print(solA)

# Part B
delay = 1
while True:
  caught_layers = traverse(layers, delay, stop=True)
  #print(delay, caught_layers)
  #if delay % 100000 == 0: print(delay)
  if len(caught_layers) == 0:
    solB = delay
    break
  delay += 1

print(solB)
