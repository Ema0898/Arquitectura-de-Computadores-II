import threading
import queue

from core import Core


class Chip:

  def __init__(self, chipNumber):
    self._cores = []
    self._threads = []
    self._queues = []
    self._chipNumber = chipNumber
    self._lock = threading.Lock()

  def startCores(self):

    for i in range(2):
      self._queues.append(queue.Queue())

    for i in range(2):
      self._cores.append(
          Core("P" + str(i), self._chipNumber, self._queues[i], self._lock))

    for i in range(2):
      self._threads.append(threading.Thread(target=self._runCore, args=(i,)))
      self._threads[i].setDaemon(True)
      self._threads[i].start()

  def _runCore(self, core):
    self._cores[core].runCore()

  def runChip(self):
    self.startCores()
    counter = 0

    while (counter < 5):
      print("Hola")

      counter += 1
