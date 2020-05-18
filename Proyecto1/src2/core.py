import queue
import threading

from cache.controllerL1 import ControllerL1
from processor import Processor


class Core(threading.Thread):
  def __init__(self, name, chipNumber, busQueueOut, busQueueIn, lock):
    threading.Thread.__init__(self)

    self._cpuQueue = queue.Queue()
    self._busQueueIn = busQueueIn
    self._busQueueOut = busQueueOut
    self._thread = 0
    self._lock = lock

    self._cacheController = ControllerL1()
    self._cpu = Processor(name, chipNumber, self._cpuQueue)
    self._cpu.setDaemon(True)
    self._cpu.start()

  def run(self):
    counter = 0
    while (counter < 5):

      cpu_msg = self._cpuQueue.get().split(',')
      bus_msg = self._busQueueIn.get()

      print("Got {} from bus".format(bus_msg))
      self._busQueueOut.put(cpu_msg)

      # self._cacheController.controlCache(
      #     "RM", cpu_msg[1], cpu_msg[2], cpu_msg[3])

      counter += 1
