from .cacheL1 import CacheL1


class ControllerL1:
  def __init__(self):
    self.cache = CacheL1()

  def controlCache(self, bus_signal, cpu_signal, direction, cpu_data):
    line = self.cache.getLine(direction)

    if line == -1:
      print("Read Miss go to the Bus and get the data from memory")
    else:
      if line.getVBit() == 0:
        print("Generate Read miss")
      else:
        self._msiMachine(bus_signal, cpu_signal, direction, cpu_data)

  def _msiMachine(self, bus_signal, cpu_signal, direction, cpu_data):
    line = self.cache.getLine(direction)

    if line.getState() == 'M':
      if bus_signal == 'RM':
        self._m_to_s(line)
        print('Stop System to Write on Memory')

      elif bus_signal == 'WM':
        self._m_to_i(line)

      elif cpu_signal == 'WRITE':
        line.setData(cpu_data)
        print('Bus Write Miss')

    elif line.getState() == 'S':
      if bus_signal == 'WM':
        self._s_to_i(line)
      elif cpu_signal == 'WRITE':
        self._s_to_m(line)
        line.setData(cpu_data)
        print('Bus Write Miss')

    elif line.getState() == 'I':
      if cpu_signal == 'WRITE':
        self._i_to_m(line)
        line.setData(cpu_data)
        print('Bus Write Miss')
      elif cpu_signal == 'READ':
        self._i_to_s(line)
        print('Bus Read Miss')

    else:
      print("Cache state error")
      return

  def _m_to_s(self, line):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)

  def _m_to_i(self, line):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)

  def _s_to_i(self, line):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)

  def _s_to_m(self, line):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)

  def _i_to_s(self, line):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)

  def _i_to_m(self, line):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
