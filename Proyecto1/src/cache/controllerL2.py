from .cacheL2 import CacheL2
from log import setup_logger


class ControllerL2:
  def __init__(self, chipOwner):
    self.cache = CacheL2()

    self._chipOwner = chipOwner

    LOG_FILENAME = 'logs/system'
    self._logging = setup_logger(LOG_FILENAME, "{}.log".format(LOG_FILENAME))

  def writeCache(self, direction, value, owner):
    logMsg = 'Escribiendo en el cache L2 para el chip {}, la dirección {} y el valor {}.'.format(
        self._chipOwner, direction, value)
    self._logging.info(logMsg)

    self.cache.setLineByIndex(direction % 4, "DS", owner, direction, value)
    # self.cache.printCache()

  def msiMachineExtL2(self, signal, direction, extOwner):
    line = self.cache.getLine(direction)

    if signal == "" or line is None:
      return

    #print("Processing L2 callback")
    if line.getState() == 'DM':
      if signal == 'WML2':
        self._dm_to_di(line)
        #print("Broadcast Invalid for L1")

        logMsg = 'Llegó un Write Miss externo para la L2 del chip {} en la dirección {} estando en DM'.format(
            self._chipOwner, direction)
        logMsg += ', invalidando los dueños. Pasando de estado DM a estado DI.'
        self._logging.info(logMsg)

        return True

      elif signal == "RML2":
        self._dm_to_ds(line, 'E')

        logMsg = 'Llegó un Read Miss externo para la L2 del chip {} en la dirección {} estando en DM'.format(
            self._chipOwner, direction)
        logMsg += ', agregando dueño {}. Pasando de estado DM a estado DS.'.format(
            extOwner)
        self._logging.info(logMsg)

    elif line.getState() == 'DS':
      if signal == 'WML2':
        self._ds_to_di(line)
        #print("Broadcast Invalid for L1")

        logMsg = 'Llegó un Write Miss externo para la L2 del chip {} en la dirección {} estando en DS'.format(
            self._chipOwner, direction)
        logMsg += ', invalidando los dueños. Pasando de estado DS a estado DI.'
        self._logging.info(logMsg)

        return True

      elif signal == "RML2":
        line.appendOwner('E')

        logMsg = 'Llegó un Read Miss externo para la L2 del chip {} en la dirección {} estando en DI'.format(
            self._chipOwner, direction)
        logMsg += ', añadiendo {} a los dueños. Pasando de estado DS a estado DI.'.format(
            extOwner)
        self._logging.info(logMsg)

    elif line.getState() == 'DI':
      if signal == "RML2":
        self._di_to_ds(line, extOwner)

        logMsg = 'Llegó un Read Miss externo para la L2 del chip {} en la dirección {} estando en DI'.format(
            self._chipOwner, direction)
        logMsg += ', añadiendo {} a los dueños. Pasando de estado DI a estado DS.'.format(
            extOwner)
        self._logging.info(logMsg)

  def msiMachineL1(self, signal, direction, cpu_data, owner):

    if signal == "NOP":
      return ("", "")

    line = self.cache.getLineByIndex(direction)
    response = ()

    if line.getState() == 'DM':
      if signal == 'RM':
        self._dm_to_ds(line, owner)
        response = (line.getData(), "")

        logMsg = 'Llegó un Read Miss para la L2 del chip {} en la dirección {} estando en DM'.format(
            self._chipOwner, direction)
        logMsg += '. Añadiendo {} a los dueños. Pasando de estado DM a estado DS.'.format(
            owner)
        self._logging.info(logMsg)

      elif signal == 'WM':
        line.setData(cpu_data)
        line.setTag(direction)
        #print('Bus Write Miss')
        response = ("WRITE", "WML2")

        logMsg = 'Llegó un Write Miss para la L2 del chip {} en la dirección {} estando en DM'.format(
            self._chipOwner, direction)
        logMsg += '. Escribiendo en Memoria. Generando Write Miss externo.'
        self._logging.info(logMsg)

    elif line.getState() == 'DS':
      if signal == 'WM':
        self._ds_to_dm(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        #print('Bus Write Miss')
        response = ("WRITE", "WML2")

        logMsg = 'Llegó un Write Miss para la L2 del chip {} en la dirección {} estando en DS'.format(
            self._chipOwner, direction)
        logMsg += '. Escribiendo en Memoria. Generando Write Miss externo.'
        logMsg += ' Dejando {} como único dueño. Pasando de estado DS a DM.'.format(
            owner)
        self._logging.info(logMsg)

      elif signal == "RM":
        line.appendOwner(owner)
        response = (line.getData(), "RML2")

        logMsg = 'Llegó un Read Miss para la L2 del chip {} en la dirección {} estando en DS'.format(
            self._chipOwner, direction)
        logMsg += '. Agregando {} a los dueños'.format(owner)
        logMsg += '. Regresando dato en Cache. Generando Read Miss externo.'
        self._logging.info(logMsg)

    elif line.getState() == 'DI':
      if signal == 'WM':
        self._di_to_dm(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        #print('Bus Write Miss')
        response = ("WRITE", "WML2")

        logMsg = 'Llegó un Write Miss para la L2 del chip {} en la dirección {} estando en DI'.format(
            self._chipOwner, direction)
        logMsg += '. Escribiendo dato en Memoria. Generando Write Miss externo.'
        logMsg += ' Dejando {} como único dueño. Pasando de estado DI a DM.'.format(
            owner)
        self._logging.info(logMsg)

      elif signal == 'RM':
        self._di_to_ds(line, owner)
        #print('Bus Read Miss')
        response = ("READ", "RML2")

        logMsg = 'Llegó un Read Miss para la L2 del chip {} en la dirección {} estando en DI'.format(
            self._chipOwner, direction)
        logMsg += '. Obteniendo dato de Memoria. Generando Write Miss externo.'
        logMsg += ' Agregando {} a los dueños. Pasando de estado DI a DS.'.format(
            owner)
        self._logging.info(logMsg)

    else:
      print("Cache state error")

    return response

  def _dm_to_ds(self, line, owner):
    line.setState('DS')
    line.appendOwner(owner)
    #print("DM to DS")

  def _dm_to_di(self, line):
    line.setState('DI')
    line.cleanOwners()
    #print("DM to DI")

  def _ds_to_dm(self, line, owner):
    line.setState('DM')
    line.cleanOwners()
    line.appendOwner(owner)
    #print("DS to DM")

  def _ds_to_di(self, line):
    line.setState('DI')
    line.cleanOwners()
    #print("DS to DI")

  def _di_to_ds(self, line, owner):
    line.setState('DS')
    line.appendOwner(owner)
    #print("DI to DS")

  def _di_to_dm(self, line, owner):
    line.setState('DM')
    line.appendOwner(owner)
    #print("DI to DM")

  def getCache(self):
    return self.cache
