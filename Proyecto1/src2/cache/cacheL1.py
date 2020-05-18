class CacheLineL1:
  def __init__(self):
    self._vBit = 0
    self._dBit = 0
    self._tag = 0
    self._data = 0
    self._state = "I"

  def getVBit(self):
    return self._vBit

  def setVBit(self, vBit):
    self._vBit = vBit

  def getDBit(self):
    return self._dBit

  def setDBit(self, dBit):
    self._dBit = dBit

  def getTag(self):
    return self._tag

  def setTag(self, tag):
    self._tag = tag

  def getData(self):
    return self._data

  def setData(self, data):
    self._data = data

  def getState(self):
    return self._state

  def setState(self, state):
    self._state = state


class CacheL1:
  def __init__(self):
    self._lines = []

    for _ in range(2):
      self._lines.append(CacheLineL1())

  def getLine(self, direction):
    for line in self._lines:
      if line.getTag() == direction:
        return line

    return -1

  def getLineByIndex(self, index):
    return self._lines[index]

  def setLineByIndex(self, index, state, tag, data, vBit, dBit):
    self._lines[index].setTag(tag)
    self._lines[index].setData(tag)
    self._lines[index].setState(state)
    self._lines[index].setVBit(vBit)
    self._lines[index].setDBit(dBit)

    if state == 'M':
      self._lines[index].setVBit(1)
      self._lines[index].setDBit(1)

    if state == 'S':
      self._lines[index].setVBit(1)
      self._lines[index].setDBit(0)

    if state == 'I':
      self._lines[index].setVBit(0)
      self._lines[index].setDBit(0)
