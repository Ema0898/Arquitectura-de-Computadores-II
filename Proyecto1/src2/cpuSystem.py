import threading
import queue
import time

from chip import Chip
from mainMemory import MainMemory


class CpuSystem(threading.Thread):

  def __init__(self, guiQueues, mainwin):
    threading.Thread.__init__(self)

    self._guiQueues = guiQueues
    self._mainwin = mainwin

    self._chipQueueIn = []
    self._chipQueueOut = queue.Queue()

    self._memory = MainMemory()
    self._chipLock = threading.Lock()

    self._l2queue1 = queue.Queue()
    self._l2queue2 = queue.Queue()

    self._chips = []

  def _startChips(self):
    for _ in range(2):
      self._chipQueueIn.append(queue.Queue())

    self._chips.append(
        Chip(0, self._chipLock, self._chipQueueIn[0], self._chipQueueOut,
             self._l2queue1, self._l2queue2, self._guiQueues[1:6], self._mainwin))

    self._chips.append(
        Chip(1, self._chipLock, self._chipQueueIn[1], self._chipQueueOut,
             self._l2queue2, self._l2queue1, self._guiQueues[6:11], self._mainwin))

    self._chips[0].start()
    self._chips[1].start()

  def run(self):
    self._startChips()
    counter = 0

    while counter < 40:

      memoryPetition = self._chipQueueOut.get().split(',')

      # print("Procesing Memory Request")
      # print("Got {} from memory".format(memoryPetition))

      memoryReturn = self._memory.controlMemory(
          memoryPetition[0], memoryPetition[1], int(memoryPetition[2]),
          int(memoryPetition[3]), memoryPetition[4])

      if memoryPetition[4] == "CH0":
        self._chipQueueIn[0].put(memoryReturn)
      elif memoryPetition[4] == "CH1":
        self._chipQueueIn[1].put(memoryReturn)

      # self._lock.acquire()

      self._guiQueues[0].put(self._memory.getMem())
      self._mainwin.event_generate('<<MEM>>')
      # time.sleep(3)

      # self._lock.release()

      counter += 1

      print("Counter = {}".format(counter))
