from math import sqrt
import re
import sys

# ==========================================

# A simple class to represent 3-vectors
# Only addition and multiplication by scalar implemented
class Vector3D:

  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def magn2(self):
    return self.x**2 + self.y**2 + self.z**2

  def __str__(self):
    return "%i, %i, %i" % (self.x, self.y, self.z)

  def __add__(self, other):
    return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

  def __mul__(self, a):
    return Vector3D(a*self.x, a*self.y, a*self.z)

  def __rmul__(self, a):
    return self.__mul__(a)

  def __repr__(self):
    return "(%i, %i, %i)" % (self.x, self.y, self.y)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.z == other.z

  def copy(self):
    return Vector3D(self.x, self.y, self.z)

# Represents a particle with 3D position, velocity, acceleration
class Particle:

  def __init__(self, ID, defstr):
    regex = 'p=<(.*),(.*),(.*)>, v=<(.*),(.*),(.*)>, a=<(.*),(.*),(.*)>'
    m = re.search(regex, defstr)
    self.ID = ID
    self.pos = Vector3D(*(int(x) for x in m.group(1,2,3)))
    self.pos0 = self.pos.copy()
    self.vel = Vector3D(*(int(x) for x in m.group(4,5,6)))
    self.vel0 = self.vel.copy()
    self.acc = Vector3D(*(int(x) for x in m.group(7,8,9)))

  # Move the particle one time step, according to the method
  # given in the problem
  def move(self):
    self.vel += self.acc
    self.pos += self.vel

  # Returns the position and velocity at time tn, following
  # the timestepping method in the problem
  def posvel_at(self, tn):
    pos = self.pos0 + tn*self.vel0 + tn*(tn+1)/2*self.acc
    vel = self.vel0 + tn*self.acc
    return pos, vel

  def __repr__(self):
    return "p%i" % (self.ID)
    #return "%i | p=(%s), v=(%s), a=(%s)" % (self.ID, self.pos, self.vel, self.acc)

  def __lt__(self, other):
    return self.ID < other.ID

# Integer square root
# (i.e. greatest integer x such that x*x <= n)
def isqrt(n):
  x = n
  y = (x + 1) // 2
  while y < x:
    x = y
    y = (x + n // x) // 2
  return x

# Checks if particles p1 and p2 collide (in the future)
# Returns the collision time if it exists. If two (positive)
# collision times exist, returns the smallest one.
# If no valid collisions found, returns None
def check_collision(p1, p2):

  # If two particles collide at time tc their 3-positions
  # at that time must be the same. In particular, the x-positions
  # must be the same, so we can use this fact to obtain candidate
  # collision times
  candidate_tcs = []

  # To do this, for particles 1 and 2, we solve x1(tc) = x2(tc)
  # for tc. Since x(t) = x0 + v0*t + t*(t+1)/2*a, we have:
  #   x01 + tc*vx01 + tc*(tc+1)/2*ax1
  #   = x02 + tc*vx02 + tc*(tc+1)/2*ax2
  # This is a quadratic in tc, A*tc^2 + B*tc + C = 0, with:
  #   A = (ax1-ax2)/2
  #   B = (vx01 + ax1/2) - (vx02 + ax2/2)
  #   C = (x01 - x02)
  # To avoid problems with non-integer division, we define
  #   A' = 2*A = (ax01-ax02)
  #   B' = 2*B = (2*vx01 + ax1) - (2*vx02 + ax2)
  # and solve the quadratic in terms of these.
  Ap = p1.acc.x - p2.acc.x
  Bp = (2*p1.vel0.x + p1.acc.x) - (2*p2.vel0.x + p2.acc.x)
  C = p1.pos0.x - p2.pos0.x

  # Check special case: A = 0 and B != 0
  # In this case the equation reduces to B*tc + C = 0, with
  # solution tc = -C/B = -2*C/B'
  if Ap == 0 and Bp != 0:
    if (-2*C) % Bp == 0:
      tc = -2*C // Bp
      candidate_tcs.append(tc)

  # Special case: A = and B = 0
  # Either the particles start in the same place, or they don't
  # ever collide.
  elif Ap == 0 and Bp == 0:
    if C == 0:
      return 0
    else:
      return None

  # In the general case, we solve the quadratic
  # The solutions are:
  #   tc = [-B +/- sqrt(B^2 - 4*A*C)] / (2*A)
  # or, in terms of A' and B':
  #   tc = [-2*B +/- sqrt((2*B)^2 - 16*A*C)] / (4*A)
  #      = [-B' +/- sqrt((B')^2 - 8*(A')*C)] / (2*A')
  # Care must be exerted since the collision time must be integer
  else:

    Dp = Bp**2 - 8*Ap*C
    if Dp < 0: return None    # No solutions
    s = isqrt(Dp)
    if s*s != Dp: return None   # Non-integer collision time
    num1 = -Bp + s
    num2 = -Bp - s

    # The solutions of the quadratic are considered candidate
    # times only if they're integer and positive
    if num1 % (2*Ap) == 0:
      tc = num1 // (2*Ap)
      if tc >= 0: candidate_tcs.append(tc)
    if s != 0 and num2 % (2*Ap) == 0:
      tc = num2 // (2*Ap)
      if tc >= 0: candidate_tcs.append(tc)

  # If no candidate collision times found, return None
  if len(candidate_tcs) == 0:
    return None

  # Otherwise, check if the candidate collision times are indeed
  # collisions by checking wherher the full 3-positions match
  valid_tcs = []
  for tc in candidate_tcs:
    pos1, vel1 = p1.posvel_at(tc)
    pos2, vel2 = p2.posvel_at(tc)
    if pos1 == pos2:
      valid_tcs.append(tc)

  # If actual collisions were found, return the minimum time
  if len(valid_tcs) == 0:
    return None
  else:
    return min(valid_tcs)

# ==========================================

# Load particles from file
count = 0
particles = []
with open(sys.argv[1]) as f:
  for line in f:
    particles.append(Particle(count, line))
    count += 1
print("%i particles loaded" % count)

# Part A

# Simulate a large number of time steps, and determine particles
# closest to origin. This works, but it's slow!

# num_steps = 10000
# for step in range(1, num_steps+1):
#   for p in particles:
#     p.move()
#   if step % (num_steps//20) == 0:
#     print(step)
# print("Done")

# Instead, analytically compute the positions of the particles at
# a very large time ...
tn = 1000000
for p in particles:
  p.pos, p.vel = p.posvel_at(tn)

# ... and determine which particle is closest to origin
closest_dist = None
closest_part = None
for p in particles:
  dist = abs(p.pos.x) + abs(p.pos.y) + abs(p.pos.z)
  if closest_dist is None or dist < closest_dist:
    closest_dist = dist
    closest_part = p.ID

solA = closest_part

# Another solution is to determine which particle has the smallest
# acceleration

# In the long run, particles with higher accelerations will always
# overtake ones with smaller acceleration, no matter their starting
# velocities and positions. If ties occur, tiebreak by starting
# velocity then by starting distance to the origin. Square magnitudes
# are used to make the comparisons.
foo = [(p.acc.magn2(), p.vel0.magn2(), p.pos0.magn2(), p) for p in particles]
foo.sort()
part = foo[0][3]
print(part.ID, part.acc.magn2())
solA_alt = part.ID


# Part B

for p in particles:
  p.removed = False

# Determine all collisions that will happen
cols = {}
for i in range(len(particles)-1):

  p1 = particles[i]
  print("Checking %s" % p1)
  for j in range(i+1,len(particles)):

    # Check collision with p2, add if found
    p2 = particles[j]
    tc = check_collision(p1, p2)
    if tc is not None:
      print(p2, tc)
      if tc not in cols:
        cols[tc] = set()
      cols[tc].add(p1)
      cols[tc].add(p2)

# Sort them by collision time
collisions = [(tc, list(cols[tc])) for tc in cols]
collisions.sort(key=lambda x: x[0])

# Then, go through each collision in order. If at least
# two of the particles are still not removed, remove them.
for tc, parts in collisions:
  print(tc, parts)
  live_parts = [x for x in parts if not x.removed]
  if len(live_parts) >= 2:
    for p in live_parts:
      p.removed = True

# Finally, count how many particles are left
count = 0
for p in particles:
  if not p.removed:
    count += 1
solB = count

print("Part A:", solA, solA_alt)
print("Part B:", solB)
