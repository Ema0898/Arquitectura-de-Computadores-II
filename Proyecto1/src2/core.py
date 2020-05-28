import queue
import threading
import time

from cache.controllerL1 import ControllerL1
from processor import Processor


class Core(threading.Thread):
  def __init__(self, name, chipNumber, busQueueOut, busQueueIn, lock):
    threading.Thread.__init__(self)

    self._cpuQueueOut = queue.Queue()
    self._cpuQueueIn = queue.Queue()
    self._busQueueIn = busQueueIn
    self._busQueueOut = busQueueOut
    self._thread = 0
    self._lock = lock
    self._name = name

    self._cacheController = ControllerL1('CH{}{}'.format(chipNumber, name))
    self._cpu = Processor(
        name, chipNumber, self._cpuQueueOut, self._cpuQueueIn)
    # self._cpu.setDaemon(True)
    self._cpu.start()

  def writeCache(self, direction, value):
    # print("Write cache for {}".format(self._name))
    self._cacheController.writeCache(direction, value)

  def run(self):
    counter = 0
    while (counter < 10):

      bus_msg = self._busQueueIn.get()

      if bus_msg != "Ready":
        msgSplit = bus_msg.split(',')
        self._cacheController.msiMachineBus(
            msgSplit[0], int(msgSplit[1]), self._name)

      self._cpuQueueIn.put("Ready")
      cpu_msg = self._cpuQueueOut.get().split(',')

      # Check processor signals
      busDataOut = self._cacheController.msiMachineProcessor(
          cpu_msg[1], int(cpu_msg[2]), int(cpu_msg[3]), self._name)

      self._lock.acquire()

      # Write to bus
      self._busQueueOut.put("{},{},{},{}".format(
          cpu_msg[0], cpu_msg[2], cpu_msg[3], busDataOut))

      self._lock.release()

      counter += 1
