import sys

rows = []
with open(sys.argv[1]) as f:
  for line in f:
    rows.append(list(map(int, line.strip().split())))

# Part A
s = 0
for row in rows:
  s += max(row) - min(row)
solA = s
print(solA)

# Part B
def process_row(row):
  for i in range(len(row)):
    for j in range(i+1,len(row)):
      n2 = max(row[i], row[j])
      n1 = min(row[i], row[j])
      if n2 % n1 == 0:
        return n2 // n1

s = 0
for row in rows:
  s += process_row(row)
solB = s
print(solB)
