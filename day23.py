import sys
from queue import Queue

# ==========================================

class Program:

  def __init__(self, instructions, part="A", verbose=False):
    self.registers = {}
    if part == "B":
      self.registers['a'] = 1
    self.instructions = instructions
    self.last_played = None
    self.ptr = 0
    self.stopped = False
    self.jumped = False
    self.verbose = verbose
    self.countA = 0

  def eval(self, thing):
    if thing.isalpha():
      if thing not in self.registers:
        self.registers[thing] = 0
      return self.registers[thing]
    else:
      return int(thing)

  def execute_next(self):

    if self.stopped:
      if self.verbose: print("Program stopped")
      return

    instruction = self.instructions[self.ptr]
    opcode = instruction[0]
    args = instruction[1:]
    if self.verbose: print(self.ptr, opcode, args)

    X = args[0]
    if len(args) == 2:
      Y = args[1]
    self.jumped = False

    if opcode == "set":
      self.registers[X] = self.eval(Y)

    elif opcode == "sub":
      self.registers[X] = self.eval(X) - self.eval(Y)

    elif opcode == "mul":
      self.countA += 1
      self.registers[X] = self.eval(X) * self.eval(Y)

    elif opcode == "jnz":
      if self.eval(X) != 0:
        self.ptr += self.eval(Y)
        self.jumped = True
        if self.verbose: print("Jumped, offset %i" % self.eval(Y))

    else:
      raise ValueError("Invalid opcode: %s" % (opcode))

    if not (self.jumped):
      self.ptr += 1

    if self.ptr < 0 or self.ptr >= len(self.instructions):
      self.stopped = True
      if self.verbose: print("Program stopping")

  def execute_all(self):

    self.ptr = 0
    while not self.stopped:
      self.execute_next()

    return self.last_played

# ==========================================

instructions = []
with open(sys.argv[1]) as f:
  for line in f:
    instructions.append(line.strip().split())

# For Part A we simply run the code

prog = Program(instructions)
prog.execute_all()
solA = prog.countA
print("Part A:", solA)

# For Part B, we first disassemble the code to make sense of it:

# b = 107900
# const c = 124900
# while True {
#   f = 1
#   for (d = 2; d <= b; d += 1) {
#     for (e = 2; e <= b; e += 1) {
#       if (d*e == b) f = 0
#     }
#   }
#   if (f == 0) h += 1
#   if (b == c) break
#   b = b + 17
# }

# We see that b starts at 107900, and c is constant and equal to
# 124900. The outer while loop makes b go from it starting value
# up to b in strides of 17, and possibly increases h depending on
# the value of f. The outer while exits (and the program ends) when
# b reaches c.

# The inner for loops make both e and d go from 2 to b. For each
# pair fo values, we check if d*e equals b. The crucial point is
# that, if b is prime, d*e == b will never happen, while if b
# is composite, d*e == b is guaranteed to happen at least once.
# Register f tracks this. After the two inner loops end, f is simply
# 1 if b is prime, 0 otherwise. And h is incremented when f is 0,
# so when b is composite.

# Therefore, all we need to do is go through the 1001 numbers from
# 107900 to 124900 in strides of 17 and determine if each number
# is composites. The solution to part B is the number of composites
# found.

from math import sqrt

# Returns the smallest factor of n, or None if n is prime
# Done through simple trial division
def get_factor(n):
  if n % 2 == 0:
    return 2
  for k in range(3, int(sqrt(n)), 2):
    if n % k == 0:
      return k
  return None

c = 124900
primes = 0
composites = 0
b = 107900
while b <= c:
  factor = get_factor(b)
  if factor is None:
    # print("%i is prime" % b)
    primes += 1
  else:
    # print("%i is composite: divisible by %i" % (b,factor))
    composites += 1
  b += 17
# print("%i primes in range" % primes)
# print("%i composites in range" % composites)
solB = composites

print("Part B:", solB)
