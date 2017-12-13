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

# ==========================================

with open(sys.argv[1]) as f:
  line = f.readline().strip()

# Part A
lengths = list(map(int, [x for x in line.split(",")]))
num_rounds = 1
numbers = do_rounds(lengths, num_rounds)
solA = numbers[0] * numbers[1]

# Part B
solB = knot_hash(line)

print(solA)
print(solB)
