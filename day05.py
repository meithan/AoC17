import sys

instructions = []
with open(sys.argv[1]) as f:
  for line in f:
    instructions.append(int(line))

def solve(instructions, part):

  N = len(instructions)
  kmax = N-1
  k = 0
  steps = 0
  while True:
    offset = instructions[k]
    if part == "A":
      instructions[k] += 1
    elif part == "B":
      if offset >= 3:
        instructions[k] -= 1
      else:
        instructions[k] += 1
    k += offset
    steps += 1
    if k < 0 or k > kmax:
      break
  return steps

print(solve(instructions[:], "A"))
print(solve(instructions[:], "B"))
