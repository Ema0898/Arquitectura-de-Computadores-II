import numpy as np
import time
import threading
import logging

from log import setup_logger


class Processor(threading.Thread):
  def __init__(self, name, chipNumber, storageOut, storageIn, mainwin, guiQueue):
    threading.Thread.__init__(self)

    self._name = name
    self._chipNumber = chipNumber
    self._instructions = ["READ", "CALC", "WRITE"]
    self._storageOut = storageOut
    self._storageIn = storageIn

    self._mainwin = mainwin
    self._guiQueue = guiQueue

    LOG_FILENAME = 'logs/system'
    self._logging = setup_logger(LOG_FILENAME, "{}.log".format(LOG_FILENAME))

  def run(self):

    counter = 0

    while True:
      self._storageIn.get()

      instr = round(np.random.normal(1, 1)) % 3
      direction = round(np.random.normal(8, 4)) % 16
      dirValue = round(np.random.normal(32768, 10000)) % 65536
      cpuSignal = self._instructions[instr]

      message = "{},{},{},{}".format(
          self._name, cpuSignal, direction, dirValue)

      self._logging.info(
          'Generando instrucción {} para el procesador {} del chip {}.'.format(
              message, self._name, self._chipNumber))

      self._storageOut.put(message)

      self._guiQueue.put_nowait(
          '{},{},{}'.format(cpuSignal, direction, dirValue))
      self._mainwin.event_generate(
          '<<{}CH{}>>'.format(self._name, self._chipNumber))

      time.sleep(5)

      counter += 1
