import numpy as np
import time
import threading
import logging

from log import setup_logger


class Processor(threading.Thread):
  def __init__(self, name, chipNumber, storageOut, storageIn):
    threading.Thread.__init__(self)

    self._name = name
    self._chipNumber = chipNumber
    self._instructions = ["READ", "CALC", "WRITE"]
    self._storageOut = storageOut
    self._storageIn = storageIn

    LOG_FILENAME = 'logs/processorsCH{}{}'.format(chipNumber, name)
    self._logging = setup_logger(LOG_FILENAME, "{}.log".format(LOG_FILENAME))

  def run(self):

    counter = 0

    while counter < 10:
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

      time.sleep(1)

      # print("Processor CH{} {} counter = {}".format(
      #     self._chipNumber, self._name, counter))

      counter += 1
