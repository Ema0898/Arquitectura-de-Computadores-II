import queue
import threading
import time

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
    self._name = name

    self._cacheController = ControllerL1()
    self._cpu = Processor(name, chipNumber, self._cpuQueue)
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
        # Write to cache
        # print(bus_msg)
        # if msgSplit[0] == "READ":
        #   # print("Writing..")
        #   self._cacheController.writeCache(int(msgSplit[1]), int(msgSplit[2]))
        # # Check bus signals
        # else:
        #print("Updating bus signals for {}".format(self._name))
        self._cacheController.msiMachine(
            msgSplit[0], int(msgSplit[1]), 0, self._name)

      cpu_msg = self._cpuQueue.get().split(',')

      # Check processor signals
      busDataOut = self._cacheController.msiMachine(
          cpu_msg[1], int(cpu_msg[2]), int(cpu_msg[3]), self._name)

      self._lock.acquire()

      # Write to bus
      self._busQueueOut.put("{},{},{},{}".format(
          cpu_msg[0], cpu_msg[2], cpu_msg[3], busDataOut))

      self._lock.release()

      counter += 1
