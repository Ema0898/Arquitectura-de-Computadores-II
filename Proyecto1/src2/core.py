import queue
import threading

from cache.controllerL1 import ControllerL1
from processor import Processor


class Core:
  def __init__(self, name, chipNumber, busQueue, lock):
    self._cpuQueue = queue.Queue()
    self._busQueue = busQueue
    self._thread = 0
    self._lock = lock

    self._cacheController = ControllerL1()
    self._cpu = Processor(name, chipNumber, self._cpuQueue)

  def _runProcessor(self):
    self._thread = threading.Thread(target=self._run)
    self._thread.setDaemon(True)
    self._thread.start()

  def _run(self):
    self._cpu.run()

  def runCore(self):
    self._runProcessor()

    counter = 0
    while (counter < 5):
      cpu_msg = self._cpuQueue.get().split(',')
      #bus_msg = self._busQueue.get()

      #print("Got {} from bus".format(bus_msg))

      self._cacheController.controlCache(
          "RM", cpu_msg[1], cpu_msg[2], cpu_msg[3])

      counter += 1
