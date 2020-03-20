from core import Core
import threading


class Chip:

  def __init__(self, chipNumber, coresNumber, storage, mainwin):
    self.cores = []
    self.threads = []
    self.chipNumber = chipNumber
    self.coresNumber = coresNumber
    self.storage = storage
    self.mainwin = mainwin

  def startCores(self):
    lock = threading.Lock()

    for i in range(self.coresNumber):
      self.cores.append(Core("P" + str(i), self.chipNumber,
                             self.storage, self.mainwin, lock))

    for i in range(self.coresNumber):
      self.threads.append(threading.Thread(target=self.run, args=(i,)))
      self.threads[i].setDaemon(True)
      self.threads[i].start()

  def run(self, core):
    self.cores[core].run()
