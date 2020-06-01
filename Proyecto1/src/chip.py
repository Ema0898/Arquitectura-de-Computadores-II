import threading
import queue
import time

from core import Core
from cache.controllerL2 import ControllerL2


class Chip(threading.Thread):

  def __init__(self, chipNumber, extLock, queueMemIn, queueMemOut, l2queue1, l2queue2, guiQueues, mainwin):
    threading.Thread.__init__(self)

    self._chipNumber = chipNumber
    self._chipName = "CH{}".format(chipNumber)
    self._lock = threading.Lock()

    self._cores = []
    self._threads = []

    self._queuesIn = queue.Queue()
    self._queuesOut = []

    self._queueMemIn = queueMemIn
    self._queueMemOut = queueMemOut
    self._extLock = extLock

    self._l2queue1 = l2queue1
    self._l2queue2 = l2queue2

    self._guiQueues = guiQueues
    self._mainwin = mainwin

    self._controller = ControllerL2(self._chipName)

  def _broadcast(self, data):
    for i in range(2):
      self._queuesOut[i].put(data)

  def _broadcastOnlyOne(self, data, owner):
    if owner == "P0":
      self._queuesOut[1].put(data)
    elif owner == "P1":
      self._queuesOut[0].put(data)

  def _startCores(self):

    for _ in range(2):
      # self._queuesIn.append(queue.Queue())
      self._queuesOut.append(queue.Queue())

    self._cores.append(
        Core("P" + str(0), self._chipNumber, self._queuesIn,
             self._queuesOut[0], self._lock, self._mainwin, self._guiQueues[1:3]))
    self._cores.append(
        Core("P" + str(1), self._chipNumber, self._queuesIn,
             self._queuesOut[1], self._lock, self._mainwin, self._guiQueues[3:5]))
    # self._cores[i].setDaemon(True)
    self._cores[0].start()
    self._cores[1].start()

  def run(self):
    self._startCores()
    counter = 0

    for i in range(2):
      self._queuesOut[i].put("Ready")

    while True:

      busPetition = self._queuesIn.get()
      busSplit = busPetition.split(',')

      # Cache L2 control
      owner = "{}.{}.{}".format(
          self._chipName, busSplit[0], int(busSplit[1]) % 2)

      busReturn, extL2Petition = self._controller.msiMachineL1(
          busSplit[3], int(busSplit[1]), int(busSplit[2]), owner)

      extL2Petition = "{},{},{}".format(extL2Petition, busSplit[1], owner)

      # Queue to main memory
      memoryMsg = "{},{},{},{},{}".format(
          busReturn, owner, busSplit[1], busSplit[2], self._chipName)

      self._extLock.acquire()
      self._queueMemOut.put(memoryMsg)
      self._extLock.release()

      memReturn = self._queueMemIn.get()

      # Queue to External L2
      self._l2queue1.put(extL2Petition)

      extL2Return = self._l2queue2.get().split(',')
      #signal, direction, extowner
      # Process external petition
      writeMissL2 = self._controller.msiMachineExtL2(
          extL2Return[0], int(extL2Return[1]), extL2Return[2])

      # broadcast signal and direction
      if writeMissL2:
        self._broadcast("{},{}".format("WM", extL2Return[1]))
      else:
        self._broadcastOnlyOne("{},{}".format(
            busSplit[3], busSplit[1]), busSplit[0])
      # self._broadcast("{},{}".format(busSplit[3], busSplit[1]))

      # Set processor data in case of Read Miss
      if busSplit[3] == "RM":
        if memReturn is not None:
          self._controller.writeCache(
              int(busSplit[1]), memReturn, [owner])
        if busSplit[0] == "P0":
          #print("Writing.. for P0 {}".format(self._chipName))
          if busReturn == "READ" and memReturn is not None:
            self._cores[0].writeCache(int(busSplit[1]), memReturn)
          else:
            self._cores[0].writeCache(int(busSplit[1]), busReturn)

        elif busSplit[0] == "P1":
          #print("Writing.. for P1 {}".format(self._chipName))
          if busReturn == "READ" and memReturn is not None:
            self._cores[1].writeCache(int(busSplit[1]), memReturn)
          else:
            self._cores[1].writeCache(int(busSplit[1]), busReturn)

      counter += 1

      self._guiQueues[2].put_nowait(self._cores[0].getCache().getLines())
      self._mainwin.event_generate('<<L1CH{}P0>>'.format(self._chipNumber))

      self._guiQueues[4].put_nowait(self._cores[1].getCache().getLines())
      self._mainwin.event_generate('<<L1CH{}P1>>'.format(self._chipNumber))

      self._guiQueues[0].put_nowait(self._controller.getCache().getLines())
      self._mainwin.event_generate('<<L2CH{}>>'.format(self._chipNumber))
      # time.sleep(1)
