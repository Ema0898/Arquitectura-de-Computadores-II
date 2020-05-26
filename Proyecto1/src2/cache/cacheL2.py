class CacheLineL2:
  def __init__(self):
    self._tag = 0
    self._data = 0
    self._state = "DI"
    self._owners = []

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

  def getOwners(self):
    return self._owners

  def setOwners(self, owners):
    self._owners = owners

  def appendOwner(self, owner):
    self._owners.append(owner)

  def cleanOwners(self):
    self._owners.clear()


class CacheL2:
  def __init__(self):
    self._lines = []

    for _ in range(4):
      self._lines.append(CacheLineL2())

  def getLine(self, direction):
    return self._lines[direction % 4]

  def getLineByIndex(self, index):
    return self._lines[index]

  def setLineByIndex(self, index, state, owners, tag, data):
    self._lines[index].setTag(tag)
    self._lines[index].setData(data)
    self._lines[index].setState(state)
    self._lines[index].setOwners(owners)
    # self.printCache()

  def printCache(self):
    for i in range(4):
      print("{}, {}, {}, {}".format(
          self._lines[i].getState(),
          self._lines[i].getOwners(),
          self._lines[i].getData(),
          self._lines[i].getTag()
      ))
