from .cacheL1 import CacheL1


class ControllerL1:
  def __init__(self):
    self.cache = CacheL1()

  def writeCache(self, direction, value):
    #print("Writing data on cache fo dir {}, value {}".format(direction, value))
    self.cache.setLineByIndex(direction % 2, "S", direction, value)
    self.cache.printCache()

  def controlCache(self, signal, direction, cpu_data, owner):
    line = self.cache.getLine(direction)

    if line.getVBit() == 0:
      #print("Generate Read miss fo dir {} and {}".format(direction, owner))
      # self.cache.printCache()
      return "RM"
    else:
      return self._msiMachine(signal, direction, cpu_data, owner)

  def _msiMachine(self, signal, direction, cpu_data, owner):
    line = self.cache.getLine(direction)

    if line.getState() == 'M':
      if signal == 'RM':
        self._m_to_s(line, owner)
        print('Stop System to Write on Memory')

      elif signal == 'WM':
        self._m_to_i(line, owner)

      elif signal == 'WRITE':
        line.setData(cpu_data)
        print('Bus Write Miss')
        return "WM"

    elif line.getState() == 'S':
      if signal == 'WM':
        self._s_to_i(line, owner)
      elif signal == 'WRITE':
        self._s_to_m(line, owner)
        line.setData(cpu_data)
        print('Bus Write Miss')
        return "WM"

    elif line.getState() == 'I':
      if signal == 'WRITE':
        self._i_to_m(line, owner)
        line.setData(cpu_data)
        print('Bus Write Miss')
        return "WM"
      elif signal == 'READ':
        self._i_to_s(line, owner)
        print('Bus Read Miss')
        return "RM"

    else:
      print("Cache state error")
      return

  def _m_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)
    print("M to S from {}".format(owner))

  def _m_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
    print("M to I from {}".format(owner))

  def _s_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
    print("S to I from {}".format(owner))

  def _s_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
    print("S to M from {}".format(owner))

  def _i_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)
    print("I to S from {}".format(owner))

  def _i_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
    print("I to M from {}".format(owner))
