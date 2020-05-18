from mainMemory import MainMemory


class Bus:
  def __init__(self):
    self._memory = MainMemory()

  def petition(self, owner, direction, data, request):
    if request == "WM":
      self._memory.setValue(owner, direction, data)

    elif request == "RM":
      return self._memory.getValue(direction)
