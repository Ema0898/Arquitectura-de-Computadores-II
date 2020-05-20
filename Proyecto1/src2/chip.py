import threading
import queue
import time

from core import Core
from bus import Bus


class Chip(threading.Thread):

  def __init__(self, chipNumber):
    threading.Thread.__init__(self)

    self._cores = []
    self._threads = []
    self._queuesIn = queue.Queue()
    self._queuesOut = []
    self._chipNumber = chipNumber
    self._lock = threading.Lock()
    self._bus = Bus()

    # self.guiQueue = guiQueue
    # self.mainwin = mainwin

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

      # broadcast direction and signal
      self._broadcast("{},{}".format(busSplit[3], busSplit[1]))

      busReturn = self._bus.petition(busPetition)

      if busReturn is not None:
        if busSplit[0] == "P0":
          # print("Bus return for P0 address {} {}".format(
          #     busSplit[1], busReturn))
          self._queuesOut[0].put("READ,{},{}".format(busSplit[1], busReturn))
        elif busSplit[0] == "P1":
          #print("Bus return for P1")
          self._queuesOut[1].put("READ,{},{}".format(busSplit[1], busReturn))

      # self._lock.acquire()

      # self.guiQueue.put("Hola {}".format(counter))
      # self.mainwin.event_generate('<<MessageGenerated>>')
      # time.sleep(3)

      # self._lock.release()

      counter += 1
