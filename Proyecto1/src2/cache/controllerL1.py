from .cacheL1 import CacheL1
from log import setup_logger


class ControllerL1:
  def __init__(self, owner):
    self.cache = CacheL1()

    self._chipOwner = owner

    LOG_FILENAME = 'logs/cacheL1{}'.format(self._chipOwner)
    self._logging = setup_logger(LOG_FILENAME, "{}.log".format(LOG_FILENAME))

  def writeCache(self, direction, value):
    logMsg = 'Escribiendo en el cache L1 para el chip {}, la dirección {} y el valor {}.'.format(
        self._chipOwner, direction, value)
    self._logging.info(logMsg)
    #print("Writing data on cache fo dir {}, value {}".format(direction, value))
    self.cache.setLineByIndex(direction % 2, "S", direction, value)
    # self.cache.printCache()

  def msiMachineBus(self, signal, direction, owner):
    line = self.cache.getLine(direction)

    if line is None:
      return

    if line.getState() == 'M':
      if signal == 'RM':
        self._m_to_s(line, owner)
        # print('Stop System to Write on Memory')
        logMsg = 'Obteniendo Read Miss del bus en la direccion {}, estando en el estado M'.format(
            direction)
        logMsg += ' Pasando de M a S'
        self._logging.info(logMsg)

      elif signal == 'WM':
        #print("Broadcast Switch")
        self._m_to_i(line, owner)

        logMsg = 'Obteniendo Write Miss del bus en la direccion {}, estando en el estado M'.format(
            direction)
        logMsg += ' Pasando de M a I'
        self._logging.info(logMsg)

    elif line.getState() == 'S':
      if signal == 'WM':
        #print("Broadcast Switch")
        self._s_to_i(line, owner)

        logMsg = 'Obteniendo Write Miss del bus en la direccion {}, estando en el estado S'.format(
            direction)
        logMsg += ' Pasando de S a I'
        self._logging.info(logMsg)

  def msiMachineProcessor(self, signal, direction, cpu_data, owner):
    line = self.cache.getLineByIndex(direction)
    response = "NOP"

    if line.getState() == 'M':
      if signal == 'WRITE':
        line.setData(cpu_data)
        line.setTag(direction)
        #print('Bus Write Miss')
        response = "WM"

        logMsg = 'Obteniendo Write del procesador en la direccion {} con valor {}, estando en el estado M'.format(
            direction, cpu_data)
        self._logging.info(logMsg)

    elif line.getState() == 'S':
      if signal == 'WRITE':
        self._s_to_m(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        #print('Bus Write Miss')
        response = "WM"

        logMsg = 'Obteniendo Write del procesador en la direccion {} con valor {}, estando en el estado S'.format(
            direction, cpu_data)
        logMsg += ' Pasando de S a M'
        self._logging.info(logMsg)

      elif signal == 'READ':
        response = "RM"

        logMsg = 'Obteniendo Read del procesador en la direccion {}, estando en el estado S'.format(
            direction)
        self._logging.info(logMsg)

    elif line.getState() == 'I':
      if signal == 'WRITE':
        self._i_to_m(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        # print('Bus Write Miss')
        response = "WM"

        logMsg = 'Obteniendo Write del procesador en la direccion {} con valor {}, estando en el estado I'.format(
            direction, cpu_data)
        logMsg += ' Pasando de I a M'
        self._logging.info(logMsg)

      elif signal == 'READ':
        self._i_to_s(line, owner)
        # print('Bus Read Miss')
        response = "RM"

        logMsg = 'Obteniendo Read del procesador en la direccion {}, estando en el estado I'.format(
            direction)
        logMsg += ' Pasando de I a S'
        self._logging.info(logMsg)

    else:
      print("Cache state error")

    return response

  def _m_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)
    #print("M to S from {}".format(owner))

  def _m_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
    #print("M to I from {}".format(owner))

  def _s_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
    #print("S to I from {}".format(owner))

  def _s_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
    #print("S to M from {}".format(owner))

  def _i_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)
    #print("I to S from {}".format(owner))

  def _i_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
    #print("I to M from {}".format(owner))

  def getCache(self):
    return self.cache
