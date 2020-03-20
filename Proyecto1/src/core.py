import numpy as np
import time


class Core:
  def __init__(self, name, chipNumber, storage, mainwin, lock):

    self.name = name
    self.chipNumber = chipNumber
    self.instructions = ["READ", "CALC", "WRITE"]
    self.storage = storage
    self.mainwin = mainwin
    self.lock = lock

  def run(self):

    counter = 0

    while counter < 5:
      instr = round(np.random.normal(1, 1)) % 3
      message = ""

      if (instr == 0):
        dir = round(np.random.normal(8, 4)) % 16
        message = '{},{}: {} {}'.format(
            self.name, self.chipNumber, self.instructions[instr], dir)
      elif (instr == 1):
        message = '{},{}: {}'.format(
            self.name, self.chipNumber, self.instructions[instr])
      else:
        dir = round(np.random.normal(8, 4)) % 16
        value = round(np.random.normal(32768, 10000)) % 65536
        message = '{},{}: {} {};{}'.format(
            self.name, self.chipNumber, self.instructions[instr], dir, value)

      counter += 1

      self.lock.acquire()

      print(message)
      self.storage.put(message)
      self.mainwin.event_generate('<<MessageGenerated>>')
      time.sleep(3)

      self.lock.release()
