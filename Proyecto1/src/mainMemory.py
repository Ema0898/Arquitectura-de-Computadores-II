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

    LOG_FILENAME = 'logs/system'
    self._logging = setup_logger(LOG_FILENAME, "{}.log".format(LOG_FILENAME))

    for _ in range(16):
      self._mem.append(MemoryLine())

  def controlMemory(self, signal, owner, direction, value, chip):
    if signal == "WRITE":
      #print("Write data to memory from {}".format(chip))
      self._mem[direction].setData(value)
      self._mem[direction].setOwner("{}".format(owner))

      logMsg = "Escribiendo en memoria principal {} en la direccion {} y para el dueño {}".format(
          value, direction, owner)
      self._logging.info(logMsg)

    elif signal == "READ":
      #print("Returning data from memory to {}".format(chip))
      logMsg = "Retornando el valor de memoria principal para la direccion {}".format(
          direction)
      self._logging.info(logMsg)

      return self._mem[direction].getData()

  def getMem(self):
    return self._mem
