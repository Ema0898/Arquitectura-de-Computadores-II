import threading
import queue

from core import Core
from cache.controllerL2 import ControllerL2


class Chip(threading.Thread):

  def __init__(self, chipNumber, queueMemIn, queueMemOut):
    threading.Thread.__init__(self)

    self._cores = []
    self._threads = []
    self._queuesIn = queue.Queue()
    self._queuesOut = []
    self._chipNumber = chipNumber
    self._lock = threading.Lock()
    self._chipName = "CH{}".format(chipNumber)
    self._queueMemIn = queueMemIn
    self._queueMemOut = queueMemOut

    self._controller = ControllerL2()

  def _broadcast(self, data):
    for i in range(2):
      self._queuesOut[i].put(data)

  def _startCores(self):

    for i in range(2):
      # self._queuesIn.append(queue.Queue())
      self._queuesOut.append(queue.Queue())

      self._cores.append(
          Core("P" + str(i), self._chipNumber, self._queuesIn, self._queuesOut[i], self._lock))
      # self._cores[i].setDaemon(True)
      self._cores[i].start()

  def run(self):
    self._startCores()
    counter = 0

    for i in range(2):
      self._queuesOut[i].put("Ready")

    while (counter < 20):

      busPetition = self._queuesIn.get()
      busSplit = busPetition.split(',')

      # Cache L2 control
      owner = "{}.{}.{}".format(
          self._chipName, busSplit[0], int(busSplit[1]) % 2)

      busReturn, _ = self._controller.msiMachineL1(
          busSplit[3], int(busSplit[1]), int(busSplit[2]), owner)

      # Queue to main memory
      memoryMsg = "{},{},{},{}".format(
          busReturn, owner, busSplit[1], busSplit[2])
      self._queueMemOut.put(memoryMsg)

      memReturn = self._queueMemIn.get()

      # Queue to External L2

      # broadcast direction and signal
      self._broadcast("{},{}".format(busSplit[3], busSplit[1]))

      # Set processor data in case of Read Miss
      if busSplit[3] == "RM":
        if memReturn is not None:
          self._controller.writeCache(
              int(busSplit[1]), memReturn, [owner])
        if busSplit[0] == "P0":
          if busReturn == "READ" and memReturn is not None:
            self._cores[0].writeCache(int(busSplit[1]), memReturn)
          else:
            self._cores[0].writeCache(int(busSplit[1]), busReturn)

        elif busSplit[0] == "P1":
          if busReturn == "READ" and memReturn is not None:
            self._cores[0].writeCache(int(busSplit[1]), memReturn)
          else:
            self._cores[0].writeCache(int(busSplit[1]), busReturn)

      counter += 1
