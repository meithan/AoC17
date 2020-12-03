import sys

with open(sys.argv[1]) as f:
  banks = list(map(int, f.readline().strip().split()))

seen = {}
seen[tuple(banks)] = 0

N = len(banks)
cycles = 0
while True:

  blocks = max(banks)
  idxmax = banks.index(blocks)

  banks[idxmax] = 0
  k = (idxmax + 1) % N
  for i in range(blocks):
    banks[k] += 1
    k = (k + 1) % N
  #print(banks)

  cycles += 1
  if tuple(banks) in seen:
    solA = cycles
    solB = cycles - seen[tuple(banks)]
    break
  else:
    seen[tuple(banks)] = cycles

print(solA)
print(solB)
