from .cacheL2 import CacheL2


class ControllerL2:
  def __init__(self):
    self.cache = CacheL2()

  def writeCache(self, direction, value, owner):
    self.cache.setLineByIndex(direction % 4, "DS", owner, direction, value)
    self.cache.printCache()

  def controlCache(self, signal, direction, cpu_data, owner, extOwner):
    line = self.cache.getLine(direction)

    if line.getState() == "DI":
      return "READ"
    else:
      return self._msiMachine(signal, direction, cpu_data, owner, extOwner)

  def _msiMachine(self, signal, direction, cpu_data, owner, extOwner):
    line = self.cache.getLine(direction)

    if line.getState() == 'DM':
      if signal == 'RM':
        self._dm_to_ds(line, owner)
        return line.getData()

      elif signal == 'WM':
        line.setData(cpu_data)
        print('Bus Write Miss')
        return ("WRITE", "WML2")

      elif signal == 'WML2':
        self._dm_to_di(line)
        print("Broadcast Invalid for L1")

      elif signal == "RML2":
        self._dm_to_ds(line, extOwner)

    elif line.getState() == 'DS':
      if signal == 'WM':
        self._ds_to_dm(line, owner)
        line.setData(cpu_data)
        print('Bus Write Miss')
        return ("WRITE", "WML2")

      elif signal == "RM":
        line.appendOwner(owner)
        return (line.getData(), "RML2")

      elif signal == 'WML2':
        self._ds_to_di(line)
        print("Broadcast Invalid for L1")

      elif signal == "RML2":
        line.appendOwner(extOwner)

    elif line.getState() == 'DI':
      if signal == 'WM':
        self._di_to_dm(line, owner)
        line.setData(cpu_data)
        print('Bus Write Miss')
        return ("WRITE", "WML2")

      elif signal == 'RM':
        self._di_to_ds(line, owner)
        print('Bus Read Miss')
        return ("READ", "RML2")

      elif signal == "RML2":
        self._di_to_ds(line, extOwner)

    else:
      print("Cache state error")
      return

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