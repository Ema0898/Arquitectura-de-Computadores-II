import threading
import queue
import time

from chip import Chip
from mainMemory import MainMemory


class CpuSystem(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)

    # self.guiQueue = guiQueue
    # self.mainwin = mainwin
    # self._lock = threading.Lock()

    self._chipQueueIn = queue.Queue()
    self._chipQueueOut = queue.Queue()

    self._memory = MainMemory()

    self._chip = Chip(0, self._chipQueueIn, self._chipQueueOut)
    self._chip.start()

  def run(self):
    counter = 0

    while counter < 20:

      memoryPetition = self._chipQueueOut.get().split(',')

      #print("Procesing Memory Request")
      #print("Got {} from memory".format(memoryPetition))

      memoryReturn = self._memory.controlMemory(
          memoryPetition[0], memoryPetition[1], int(memoryPetition[2]), int(memoryPetition[3]))

      self._chipQueueIn.put(memoryReturn)

      # self._lock.acquire()

      # self.guiQueue.put("Hola {}".format(counter))
      # self.mainwin.event_generate('<<MessageGenerated>>')
      # time.sleep(3)

      # self._lock.release()

      counter += 1

      print("Counter = {}".format(counter))
