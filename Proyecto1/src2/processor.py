import numpy as np
import time


class Processor:
  def __init__(self, name, chipNumber, storage):

    self._name = name
    self._chipNumber = chipNumber
    self._instructions = ["READ", "CALC", "WRITE"]
    self._storage = storage

  def run(self):

    counter = 0

    while counter < 5:
      instr = round(np.random.normal(1, 1)) % 3
      direction = round(np.random.normal(8, 4)) % 16
      dirValue = round(np.random.normal(32768, 10000)) % 65536
      cpuSignal = self._instructions[instr]

      message = "{},{},{},{}".format(
          self._name, cpuSignal, direction, dirValue)

      self._storage.put(message)

      time.sleep(1)

      counter += 1
