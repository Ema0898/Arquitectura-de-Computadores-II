from cache.cacheL1 import CacheL1
from cache.controllerL1 import ControllerL1
from core import Core
from bus import Bus
from chip import Chip
from cache.controllerL2 import ControllerL2
from cpuSystem import CpuSystem

# cache = CacheL1()
# lines = cache.getLines()

# for i in range(2):
#   lines[i].setVBit(1)
#   lines[i].setDBit(0)
#   lines[i].setTag(8 + i)
#   lines[i].setData(2 * i)

# lines[0].setState('M')
# lines[1].setState('S')

# for line in cache.getLines():
#   print("{}, {}, {}, {}, {}".format(line.getVBit(),
#                                     line.getDBit(), line.getTag(), line.getData(), line.getState()))

# chip1 = Chip(0)
# chip1.startCores()
# chip1.run()

# if __name__ == '__main__':
#   controller = ControllerL1()
#   line = controller.cache.getLine(0)
#   line.setState('M')
#   controller.controlCache(0, 'WM', 'READ', 25)

#   print("{}, {}, {}, {}, {}".format(line.getVBit(),
#                                     line.getDBit(), line.getTag(), line.getData(), line.getState()))

# core = Core("P1", 0, None, None)
# core.run()

# bus = Bus()
# bus.petition("P1", 12, 150, "WM")
# print(bus.petition("P1", 12, 150, "RM"))

# core = Core("P0", 0, None, None)
# core.runCore()

# chip = Chip(0)
# chip.start()
# chip.join()

# controller = ControllerL2()
# controller.writeCache(7, 100, ["CH0,P0,1"])
# hola, _ = controller.controlCache("RM", 7, 100, "CH0,P1,0", None)
# print(hola)
# controller.getCache().printCache()

cpu = CpuSystem()
cpu.start()
cpu.join()
