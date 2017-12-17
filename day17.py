import sys

# ==========================================


# ==========================================

with open(sys.argv[1]) as f:
  steps = int(f.readline())

# Part A
pos = 0
buff = [0]
# repeats = 10
repeats = 2017
for x in range(1,repeats+1):
  # print("\n", buff, pos)
  pos = (pos + steps) % x
  # print(pos)
  buff.insert(pos+1, x)
  pos += 1
  # print("->", buff, pos)

# print(buff[pos-3:pos+3+1])
solA = buff[pos+1]

# Part B
# We don't do the insertions, just track the position
pos = 0
repeats = 50000000
solB = None
for x in range(1,repeats+1):
  pos = (pos + steps + 1) % x
  if pos == 0:
    solB = x
  # if x % 1000000 == 0: print(x)

print(solA)
print(solB)
