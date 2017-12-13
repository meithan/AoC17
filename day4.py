import sys

passphrases = []
with open(sys.argv[1]) as f:
  for line in f:
    passphrases.append(line.strip().split())

def solve(passphrases, part):
  count = 0
  for words in passphrases:
    if part == "B":
      for i in range(len(words)):
        words[i] = sorted(words[i])
    words.sort()   # O(n log n)
    is_valid = True
    for i in range(len(words)-1):   # O(n)
      if words[i] == words[i+1]:
        is_valid = False
        break
    if is_valid: count += 1
  return count

print(solve(passphrases, "A"))
print(solve(passphrases, "B"))
