import sys
from functools import reduce

# ==========================================

def reverse(numbers, start, length):
  N = len(numbers)
  for k in range(length//2):
    i1 = (start + k) % N
    i2 = (start + length - k - 1) % N
    tmp = numbers[i1]
    numbers[i1] = numbers[i2]
    numbers[i2] = tmp
    #print(k,i1,i2)

def do_rounds(lengths, num_rounds):

  numbers = list(range(256))
  N = len(numbers)
  pos = 0
  skip = 0
  #print(numbers)
  for rnd in range(num_rounds):
    for length in lengths:
      #print("> pos=%i, length=%i, skip=%i" % (pos, length, skip))
      reverse(numbers, pos, length)
      pos = (pos + length + skip) % N
      skip += 1
      #print(numbers, pos)
  return numbers

def knot_hash(inputstr):

    lengths = [ord(c) for c in inputstr] + [17, 31, 73, 47, 23]
    sparse_hash = do_rounds(lengths, 64)
    dense_hash = [reduce(lambda x,y: x^y, sparse_hash[i*16:(i+1)*16]) for i in range(16)]
    final_hash = "".join(["%02x" % x for x in dense_hash])
    return final_hash

def get_neighs(i,j):
  neighs = []
  if i+1 <= 127: neighs.append((i+1,j))
  if i-1 >= 0: neighs.append((i-1,j))
  if j+1 <= 127: neighs.append((i,j+1))
  if j-1 >= 0: neighs.append((i,j-1))
  return neighs

# ==========================================

for line in sys.stdin:
  key = line.strip()

# Part A
memory = []
used_squares = 0
for i in range(128):
  hashed = knot_hash(key + "-%i" % i)
  binary_str = "".join(["{0:04b}".format(int(d,16)) for d in hashed])
  used_squares += binary_str.count("1")
  memory.append(binary_str)

solA = used_squares
print(solA)

# Part B
visited = set()
regions = 0
for i0 in range(128):
  for j0 in range(128):
    if memory[i0][j0] == '0': continue
    elif (i0,j0) not in visited:
      regions += 1
      to_check = [(i0,j0)]
      while len(to_check) > 0:
        i,j = to_check.pop()
        visited.add((i,j))
        for ni, nj in get_neighs(i,j):
          if (ni,nj) not in visited and memory[ni][nj] == '1':
            to_check.append((ni,nj))
print(regions)
