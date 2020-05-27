from .cacheL2 import CacheL2


class ControllerL2:
  def __init__(self):
    self.cache = CacheL2()

  def writeCache(self, direction, value, owner):
    self.cache.setLineByIndex(direction % 4, "DS", owner, direction, value)
    self.cache.printCache()

  def msiMachineL2(self, signal, direction, extOwner):
    line = self.cache.getLine(direction)

    if line.getState() == 'DM':
      if signal == 'WML2':
        self._dm_to_di(line)
        #print("Broadcast Invalid for L1")

      elif signal == "RML2":
        self._dm_to_ds(line, extOwner)

    elif line.getState() == 'DS':
      if signal == 'WML2':
        self._ds_to_di(line)
        print("Broadcast Invalid for L1")

      elif signal == "RML2":
        line.appendOwner(extOwner)

    elif line.getState() == 'DI':
      if signal == "RML2":
        self._di_to_ds(line, extOwner)

  def msiMachineL1(self, signal, direction, cpu_data, owner):

    if signal == "NOP":
      return ("", "")

    line = self.cache.getLine(direction)
    response = ()

    if line.getState() == 'DM':
      if signal == 'RM':
        self._dm_to_ds(line, owner)
        response = (line.getData(), "")

      elif signal == 'WM':
        line.setData(cpu_data)
        #print('Bus Write Miss')
        response = ("WRITE", "WML2")

    elif line.getState() == 'DS':
      if signal == 'WM':
        self._ds_to_dm(line, owner)
        line.setData(cpu_data)
        #print('Bus Write Miss')
        response = ("WRITE", "WML2")

      elif signal == "RM":
        line.appendOwner(owner)
        response = (line.getData(), "RML2")

    elif line.getState() == 'DI':
      if signal == 'WM':
        self._di_to_dm(line, owner)
        line.setData(cpu_data)
        #print('Bus Write Miss')
        response = ("WRITE", "WML2")

      elif signal == 'RM':
        self._di_to_ds(line, owner)
        #print('Bus Read Miss')
        response = ("READ", "RML2")

    else:
      print("Cache state error")

    return response

  def _dm_to_ds(self, line, owner):
    line.setState('DS')
    line.appendOwner(owner)
    print("DM to DS")

  def _dm_to_di(self, line):
    line.setState('DI')
    line.cleanOwners()
    print("DM to DI")

  def _ds_to_dm(self, line, owner):
    line.setState('DM')
    line.cleanOwners()
    line.appendOwner(owner)
    print("DS to DM")

  def _ds_to_di(self, line):
    line.setState('DI')
    line.cleanOwners()
    print("DS to DI")

  def _di_to_ds(self, line, owner):
    line.setState('DS')
    line.appendOwner(owner)
    print("DI to DS")

  def _di_to_dm(self, line, owner):
    line.setState('DM')
    line.appendOwner(owner)
    print("DI to DM")

  def getCache(self):
    return self.cache
