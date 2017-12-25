from collections import defaultdict
import re
import sys

# ==========================================

# Holds a transition rule: what value to write on the tape,
# which direction to move, and the next state of the machine
class Rule:
  def __init__(self, write_value, move, next_state):
    self.write_value = write_value
    self.move = move
    self.next_state = next_state
  def __repr__(self):
    return "(%i, %+i, %s)" % (self.write_value, self.move, self.next_state)

# Simulate a Turing Machine :D
class TuringMachine:

  def __init__(self, def_file):

    self.state = None
    self.start_state = None
    self.pos = 0
    self.tape = defaultdict(lambda: 0)
    self.state_table = {}
    self.checksum = None

    # Parse the state table from the definition file
    # The state table is a dict containing states as keys.
    # Associated to each current state is another dict which
    # holds state transition rules indexed by the possible
    # values on the tape.
    with open(def_file) as f:

      line = f.readline()
      match = re.search("^Begin in state (.)\.$", line)
      if match is None: raise Exception("Couldn't parse start state")
      self.start_state = match.group(1)
      print("Start state:", self.start_state)

      line = f.readline()
      match = re.search("^Perform a diagnostic checksum after (.*) steps\.", line)
      if match is None: raise Exception("Couldn't parse diagnostic steps")
      self.diag_steps = int(match.group(1))
      print("Diagnostic after %i steps" % self.diag_steps)

      while True:
        line = f.readline()
        if not line: break

        if "In state" in line:

          match = re.search("In state (.):$", line)
          if match is None: raise Exception("Couldn't parse line: %s" % line)
          state = match.group(1)

          rules = {}
          for i in range(2):

            line = f.readline()
            match = re.search("If the current value is (.)", line)
            if match is None: raise Exception("Couldn't parse line: %s" % line)
            value = int(match.group(1))

            line = f.readline()
            match = re.search("Write the value (.)", line)
            if match is None: raise Exception("Couldn't parse line: %s" % line)
            write = int(match.group(1))

            line = f.readline()
            match = re.search("Move one slot to the (.*).", line)
            if match is None: raise Exception("Couldn't parse line: %s" % line)
            if match.group(1) == "right": move = +1
            else: move = -1

            line = f.readline()
            match = re.search("Continue with state (.*).", line)
            if match is None: raise Exception("Couldn't parse line: %s" % line)
            next_state = match.group(1)

            rules[value] = Rule(write, move, next_state)

          self.state_table[state] = rules

    print("Loaded state table:")
    print(self.state_table)
    self.state = self.start_state

  # Do one step of the machine
  def do_step(self):

    tape_value = self.tape[self.pos]
    rule = self.state_table[self.state][tape_value]
    self.tape[self.pos] = rule.write_value
    self.pos += rule.move
    self.state = rule.next_state

  # Run the machine, until diag_steps is reached
  def run(self):

    self.steps = 0
    while True:
      self.do_step()
      self.steps += 1
      if self.steps == self.diag_steps:
        break

  # Computes the ckechsum --the number of ones-- of the current tape
  def get_checksum(self):
    checksum = 0
    for values in self.tape.values():
      if values == 1:
        checksum += 1
    return checksum

# ==========================================

# Init Turing machine with file
machine = TuringMachine(sys.argv[1])
machine.run()
checksum = machine.get_checksum()
solA = checksum

print("Part A:", solA)
