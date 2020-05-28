import numpy as np

from log import setup_logger


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

    LOG_FILENAME = 'logs/memory'
    self._logging = setup_logger(LOG_FILENAME, "{}.log".format(LOG_FILENAME))

    for i in range(16):
      self._mem.append(MemoryLine())
      self._mem[i].setData(round(np.random.normal(32768, 10000)) % 65536)

  def controlMemory(self, signal, owner, direction, value, chip):
    if signal == "WRITE":
      #print("Write data to memory from {}".format(chip))
      self._mem[direction].setData("{}{}".format(chip, owner))
      self._mem[direction].setOwner(owner)

      logMsg = "Escribiendo {} en la direccion {} y para el dueño {}".format(
          value, direction, owner)
      self._logging.info(logMsg)

    elif signal == "READ":
      #print("Returning data from memory to {}".format(chip))
      logMsg = "Retornando el valor para la direccion {}".format(direction)
      self._logging.info(logMsg)

      return self._mem[direction].getData()
