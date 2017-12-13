import sys

with open(sys.argv[1]) as f:
  numbers = f.readline().strip()

# Part A
s = 0
N = len(numbers)
for k in range(N):
  knext = (k+1) % N
  if numbers[k] == numbers[knext]:
    s += int(numbers[k])
solA = s
print(solA)

# Part B
s = 0
N = len(numbers)
for k in range(N):
  knext = (k + N//2) % N
  if numbers[k] == numbers[knext]:
    s += int(numbers[k])
solB = s
print(solB)
