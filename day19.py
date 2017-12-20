import sys

# ==========================================

# Returns the next coordinate from (row,col) moving in direction direc
# Does not check for out of bounds coords
def get_next_coords(row, col, direc):
  if direc == "down": return row + 1, col
  elif direc == "up": return row - 1, col
  elif direc == "left": return row, col - 1
  elif direc == "right":return row, col + 1

# Returns the reverse of the given direction
def reverse(direc):
  if direc == "down": return "up"
  elif direc == "up": return "down"
  elif direc == "left": return "right"
  elif direc == "right": return "left"

# ==========================================

direcs = ["down", "up", "left", "right"]

# Get tubes in a 2D array
tubes = []
numrows = 0
numcols = None
with open(sys.argv[1]) as f:
  for line in f:
    row = [x for x in line.strip("\n")]
    if numcols is None:
      numcols = len(row)
    else:
      assert(len(row) == numcols)
    tubes.append(row)
    numrows += 1

# Initial values
# We start at (0,x) where x is the column of the first (and only)
# pipe in the first row, and moving down
row = 0
col = tubes[0].index("|")
direc = "down"
letters = ""
steps = 1

while True:

  symbol = tubes[row][col]
  print(row,col,symbol, direc)

  # When we stop on a letter append it to seen letters if we
  # haven't seen it yet (we could run into a letter twice if it's
  # located at an intersection)
  if symbol.isalpha():
    if symbol not in letters:
      letters += symbol

  # Stopping on a | or - we just keep going with no direction change
  elif symbol in ["|", "-"]:
    pass

  # Stopping on a +, we change direction
  # We check what's on the three directions we can in principle go
  # and go where the path continues (making sure not to double back)
  elif symbol == "+":
    for next_direc in [x for x in direcs if x != reverse(direc)]:
      next_row, next_col = get_next_coords(row, col, next_direc)
      if 0 <= next_row < numrows and 0 <= next_col < numcols \
      and tubes[next_row][next_col] != " ":
        print(next_direc, tubes[next_row][next_col])
        direc = next_direc
        break

  # If the next position is empty, we've reached the end,
  # so don't move anymore and break out of the loop
  next_row, next_col = get_next_coords(row, col, direc)
  if tubes[next_row][next_col] == " ":
    break

  # Otherwise, move one step in the current direction
  else:
    row, col = next_row, next_col
    steps += 1

solA = letters
print(solA)

solB = steps
print(solB)
