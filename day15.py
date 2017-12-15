import sys

# ==========================================

class Generator:
  def __init__(self, factor, start_value, multiple=None):
    self.factor = factor
    self.start_value = start_value
    self.multiple = multiple
    self.state = start_value
  def next(self):
    self.state = (self.state * self.factor) % 2147483647
    if self.multiple is not None:
      while self.state % self.multiple != 0:
        self.state = (self.state * self.factor) % 2147483647
    return self.state

def compare_generators(genA, genB, numpairs):
  count = 0
  for i in range(numpairs):
    value_A = genA.next()
    value_B = genB.next()
    # binstr_A = "{0:016b}".format(value_A)[-16:]
    # binstr_B = "{0:016b}".format(value_B)[-16:]
    # if binstr_A == binstr_B:
    if value_A & 0xffff == value_B & 0xffff:
      count += 1
    if i % (numpairs/10) == 0:
      print(i, count)
  return count

# ==========================================

with open(sys.argv[1]) as f:
  genA_start = int(f.readline().strip().split()[4])
  genB_start = int(f.readline().strip().split()[4])

# Part A
genA = Generator(16807, genA_start)
genB = Generator(48271, genB_start)
solA = compare_generators(genA, genB, 40000000)
print("solA=",solA)

# Part B
genA = Generator(16807, genA_start, 4)
genB = Generator(48271, genB_start, 8)
solB = compare_generators(genA, genB, 5000000)
print("solB=",solB)
