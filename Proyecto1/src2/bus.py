from cache.controllerL2 import ControllerL2


class Bus:
  def __init__(self):
    self._controller = ControllerL2()

  def getController(self):
    return self._controller

  def petition(self, signal, direction, data, owner):
    # owner, direction, value, signal
    return self._controller.msiMachine(signal, direction, data, owner, None)
