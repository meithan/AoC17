import sys

# ==========================================

def parse_move(movestr):
  move_type = movestr[0]
  if move_type == "s":
    num = int(movestr[1:])
    move = ("s", num)
  elif move_type == "x":
    posA, posB = tuple(map(int, movestr[1:].split("/")))
    move = ("x", posA, posB)
  elif move_type == "p":
    progA, progB = tuple(movestr[1:].split("/"))
    move = ("p", progA, progB)
  return move

def swap(programs, posA, posB):
  pos1 = min(posA, posB)
  pos2 = max(posA, posB)
  return programs[:pos1] + programs[pos2] + programs[pos1+1:pos2] + programs[pos1] + programs[pos2+1:]

def apply_move(programs, move):

  move_type = move[0]

  if move_type == "s":
    num = move[1]
    # print(move_type, num)
    # print(programs[-num:], programs[:-num])
    new_programs = programs[-num:] + programs[:-num]

  elif move_type == "x":
    # print(move_type, move[1], move[2])
    new_programs = swap(programs, move[1], move[2])

  elif move_type == "p":
    for k in range(len(programs)):
      if programs[k] == move[1]:
        idxA = k
      elif programs[k] == move[2]:
        idxB = k
    # print(move_type, idxA, idxB)
    new_programs = swap(programs, idxA, idxB)

  return new_programs

# ==========================================

with open(sys.argv[1]) as f:
  moves = f.readline().strip().split(",")

# Parse moves
for i in range(len(moves)):
  moves[i] = parse_move(moves[i])
# print(moves)

# Initial, dumb way to solve it
# But hey, at least it works. Runs in about 5 minutes.

# #programs = "abcde"
# programs = "abcdefghijklmnop"
# cache = {}
# cached_count = 0
# N = 10000000
# for it in range(1,N+1):
#   if programs in cache:
#     programs = cache[programs]
#     cached_count += 1
#   else:
#     old_programs = programs
#     for move in moves:
#       programs = apply_move(programs, move)
#       # print(programs)
#     cache[old_programs] = programs
#   if it == 1:
#     solA = programs
#   elif it % (N/100) == 0:
#     print("{:,d} {:d} {:d}".format(it, len(cache), cached_count))
# solB = programs
# #print(cached_count, len(cache))

# First find the cycle
programs = "abcdefghijklmnop"
cache = {}
it = 0
while True:
  old_programs = programs
  for move in moves:
    programs = apply_move(programs, move)
  cache[old_programs] = (programs, it)
  it += 1
  #print(it, old_programs, "->", programs)
  if programs in cache:
    seen_programs = programs
    break
  if it == 1:
    solA = programs

# Then rebuild the cycle as an array
cycle_length = it
#print(seen_programs, "seen, cycle of length %i found" % cycle_length)
cycle_offset = cache[seen_programs][1]
cycle = [seen_programs]
for i in range(cycle_length-1):
  programs = cache[programs][0]
  cycle.append(programs)

# Finally, simply predict billionth iteration
target_it = 1000000000
solB = cycle[(target_it - cycle_offset) % cycle_length]

print(solA)
print(solB)
