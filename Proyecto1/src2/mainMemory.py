import numpy as np


class MemoryLine:
  def __init__(self):
    self._owner = 0
    self._data = 0

  def getOwner(self):
    return self._owner

  def setOwner(self, owner):
    self._owner = owner

  def getData(self):
    return self._data

  def setData(self, data):
    self._data = data


class MainMemory:
  def __init__(self):
    self._mem = []

    for i in range(16):
      self._mem.append(MemoryLine())
      self._mem[i].setData(round(np.random.normal(32768, 10000)) % 65536)

  def getValue(self, direction):
    return self._mem[direction].getData()

  def setValue(self, owner, direction, value):
    self._mem[direction].setData(value)
    self._mem[direction].setOwner(owner)