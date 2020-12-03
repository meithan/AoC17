import sys

with open(sys.argv[1]) as f:
  lines = f.readlines()

stream = lines[0]
# stream = lines[1]
# stream = lines[2]
# stream = lines[3]
# stream = lines[4]

N = len(stream)
score = 0
level = 0
in_garbage = False
i = 0
garbabe_count = 0
while i < N:

  if in_garbage:
    if stream[i] == "!":
      i += 1
    elif stream[i] == ">":
      in_garbage = False
    else:
      garbabe_count += 1

  elif not in_garbage:
    if stream[i] == "<":
      in_garbage = True
    elif stream[i] == "{":
      level += 1
    elif stream[i] == "}":
      score += level
      level -= 1

  i += 1

solA = score
solB = garbabe_count
print(solA)
print(solB)
