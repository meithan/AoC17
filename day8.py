import sys

# ==========================================

class Instruction:
  def __init__(self, s):
    tokens = s.strip().split()
    self.reg = tokens[0]
    self.op = tokens[1]
    self.val = int(tokens[2])
    self.condreg = tokens[4]
    self.comp = tokens[5]
    self.condval = int(tokens[6])
  def __repr__(self):
    return "%s %s %i if %s %s %i" % (self.reg, self.op, self.val, self.condreg, self.comp, self.condval)

# ==========================================

with open(sys.argv[1]) as f:
  lines = f.readlines()

# Get instructions, register names
instructions = []
registers = {}
for line in lines:
  ins = Instruction(line)
  instructions.append(ins)
  if ins.reg not in registers:
    registers[ins.reg] = 0

# Apply instructions
globalmax = None
for ins in instructions:
  cond = "registers['%s'] %s %i" % (ins.condreg, ins.comp, ins.condval)
  if (eval(cond) == True):
    if ins.op == "inc":
      registers[ins.reg] += ins.val
    elif ins.op == "dec":
      registers[ins.reg] -= ins.val
    if globalmax is None or registers[ins.reg] > globalmax:
      globalmax = registers[ins.reg]

solA = max(registers.values())
solB = globalmax
print(solA)
print(solB)
