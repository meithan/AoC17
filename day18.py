import sys
from queue import Queue

# ==========================================

class Program:

  def __init__(self, ID, instructions, progtype="A", otherprog=None, verbose=False):
    self.ID = ID
    self.registers = {'p':self.ID}
    self.instructions = instructions
    self.progtype = progtype
    self.messages = Queue()
    self.sent_count = 0
    self.last_played = None
    self.idx = 0
    self.stopped = False
    self.jumped = False
    self.waiting = False
    self.otherprog = otherprog
    self.verbose = verbose


  def eval(self, thing):
    if thing.isalpha():
      if thing not in self.registers:
        self.registers[thing] = 0
      return self.registers[thing]
    else:
      return int(thing)


  def execute(self, instruction):

    cmd = instruction[0]
    args = instruction[1:]
    if self.verbose: print(self.idx, cmd, args)

    X = args[0]
    if len(args) == 2:
      Y = args[1]
    self.jumped = False

    if cmd == "snd":

      if self.progtype == "A":
        if self.verbose: print("Played %s: %i" % (X, self.eval(X)))
        self.last_played = self.eval(X)

      elif self.progtype == "B":
        self.otherprog.messages.put(self.eval(X))
        self.sent_count += 1
        if self.verbose: print("Sent %i" % self.eval(X))

    elif cmd == "rcv":

      if self.progtype == "A":
        if self.eval(X) != 0:
          if self.verbose: print("Recovered frequency %i" % self.last_played)
          self.stopped = True

      elif self.progtype == "B":
        if not self.messages.empty():
          self.registers[X] = self.messages.get()
          if self.verbose: print("Received %i" % self.registers[X])
          self.waiting = False
        else:
          self.waiting = True

    elif cmd == "set":
      self.registers[X] = self.eval(Y)

    elif cmd == "add":
      self.registers[X] = self.eval(X) + self.eval(Y)

    elif cmd == "mul":
      self.registers[X] = self.eval(X) * self.eval(Y)

    elif cmd == "mod":
      self.registers[X] = self.eval(X) % self.eval(Y)

    elif cmd == "jgz":
      if self.eval(X) > 0:
        self.idx += self.eval(Y)
        self.jumped = True
        if self.verbose: print("Jumped, offset %i" % self.eval(Y))

    else:
      raise ValueError("Invalid command: %s" % (cmd))

    if not (self.jumped or self.waiting):
      self.idx += 1

    if self.idx < 0 or self.idx >= len(self.instructions):
      self.stopped = True
      if self.verbose: print("Program stopping")


  def execute_next(self):

    if not self.stopped:
      self.execute(self.instructions[self.idx])
    else:
      if self.verbose: print("Program stopped")
      else: pass


  def execute_all(self):

    self.idx = 0
    while not self.stopped:
      self.execute_next()

    return self.last_played

# ==========================================

instructions = []
with open(sys.argv[1]) as f:
  for line in f:
    instructions.append(line.strip().split())

# Part A
prog = Program(0, instructions, progtype="A", verbose=False)
solA = prog.execute_all()
print(solA)

# Part B
prog0 = Program(0, instructions, progtype="B", verbose=False)
prog1 = Program(1, instructions, progtype="B", verbose=False)
prog0.otherprog = prog1
prog1.otherprog = prog0
while not (prog0.waiting and prog1.waiting) and not (prog0.stopped and prog1.stopped):
  prog0.execute_next()
  prog1.execute_next()
  #input()

solB = prog1.sent_count
print(solB)
