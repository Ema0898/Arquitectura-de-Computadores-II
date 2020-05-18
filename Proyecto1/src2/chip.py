import threading
import queue
import time

from core import Core


class Chip(threading.Thread):

  def __init__(self, chipNumber, guiQueue, mainwin):
    threading.Thread.__init__(self)

    self._cores = []
    self._threads = []
    self._queuesIn = []
    self._queuesOut = []
    self._chipNumber = chipNumber
    self._lock = threading.Lock()

    self.guiQueue = guiQueue
    self.mainwin = mainwin

  def _startCores(self):

    for i in range(2):
      self._queuesIn.append(queue.Queue())
      self._queuesOut.append(queue.Queue())

      self._cores.append(
          Core("P" + str(i), self._chipNumber, self._queuesIn[i], self._queuesOut[i], self._lock))
      self._cores[i].setDaemon(True)
      self._cores[i].start()

  def run(self):
    self._startCores()
    counter = 0

    while (counter < 5):

      for i in range(2):
        self._queuesOut[i].put("Hola")

      print(self._queuesIn[0].get())

      self._lock.acquire()

      self.guiQueue.put("Hola {}".format(counter))
      self.mainwin.event_generate('<<MessageGenerated>>')
      time.sleep(3)

      self._lock.release()

      counter += 1
