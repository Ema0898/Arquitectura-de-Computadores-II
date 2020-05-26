from mainMemory import MainMemory


class Bus:
  def __init__(self):
    self._memory = MainMemory()

  def petition(self, request):
    #print("From bus got {}".format(request))
    data = request.split(',')
    if data[3] == "WM":
      print("Writing data to memory")
      self._memory.setValue(data[0], int(data[1]), int(data[2]))
      return None

    elif data[3] == "RM":
      #print("Returning data from memory to {}".format(data[0]))
      return self._memory.getValue(int(data[1]))
