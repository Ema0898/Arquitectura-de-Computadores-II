import tkinter as tk
import queue

from cpuSystem import CpuSystem
from table import Table

root = tk.Tk()

titlesL1 = ['Bloque', 'Estado', 'Dirección', 'Dato']
titlesL2 = ['Bloque', 'Estado', 'Dueño', 'Dirección', 'Dato']
titlesMem = ['Dirección', 'Dueño', 'Dato']

tableTitlesL1 = ['Cache L1 P0 CH0', 'Cache L1 P1 CH0',
                 'Cache L1 P0 CH1', 'Cache L1 P1 CH1']
tableTitlesL2 = ['Cache L2 CH0', 'Cache L2 CH1']
labelProcessorTitles = ['P0 CH0', 'P1 CH0', 'P0 CH1', 'P1 CH1']

bgColor = '#95a5bf'

l1Arr = []
l2Arr = []
pArr = []
tMem = None


def processProcessorLabel(storage, event, label):
  msg = storage.get().split(',')
  text = tk.StringVar()
  if msg[0] == 'READ':
    text.set('{},{}'.format(msg[0], msg[1]))
  elif msg[0] == 'CALC':
    text.set(msg[0])
  else:
    text.set('{},{},{}'.format(msg[0], msg[1], msg[2]))

  label.config(textvariable=text)


def processL1Tables(storage, event, table):
  msg = storage.get()

  for i in range(2):
    table.set(i + 1, 1, msg[i].getState())
    table.set(i + 1, 2, msg[i].getTag())
    table.set(i + 1, 3, msg[i].getData())


def processL2Tables(storage, event, table):
  msg = storage.get()

  for i in range(4):
    table.set(i + 1, 1, msg[i].getState())
    table.set(i + 1, 2, msg[i].getOwners())
    table.set(i + 1, 3, msg[i].getTag())
    table.set(i + 1, 4, msg[i].getData())


def processMemTables(storage, event, table):
  msg = storage.get()

  for i in range(16):
    table.set(i + 1, 1, msg[i].getOwner())
    table.set(i + 1, 2, msg[i].getData())


def createProcessorLabel():
  global pArr

  x1 = [30, 350, 670, 985]
  x2 = [170, 490, 810, 1130]

  y = 10
  # Procesor instructions
  for i in range(4):
    label = tk.Label(root)
    label.config(bg=bgColor, text='Procesador {}: '.format(
        labelProcessorTitles[i]))
    label.place(x=x1[i], y=y)

  for i in range(4):
    pLabel = tk.Label(root)
    # pLabel.config(bg=bgColor, text='WRITE,15,1')
    pLabel.config(bg=bgColor)
    pLabel.place(x=x2[i], y=y)
    pArr.append(pLabel)


def createL1Tables():
  global l1Arr

  offset = 320
  x = [120, 440, 760, 1080]
  y1 = 40
  y2 = 60
  # L1 tables

  for i in range(4):
    title = tk.Label(root)
    title.config(bg=bgColor, text=tableTitlesL1[i])
    title.place(x=x[i], y=y1)

  for i in range(4):
    t = Table(root, 3, 4)
    t.createTable(titlesL1, '#5696fc', 'white', True)
    t.place(x=15 + (offset * i), y=y2)
    l1Arr.append(t)


def createL2Tables():
  global l2Arr

  x1 = [295, 895]
  y1 = 160

  x2 = [150, 750]
  y2 = 180

  for i in range(2):
    title = tk.Label(root)
    title.config(bg=bgColor, text=tableTitlesL2[i])
    title.place(x=x1[i], y=y1)

  # L2 tables
  for i in range(2):
    t = Table(root, 5, 5)
    t.createTable(titlesL2, '#5696fc', 'white', True)
    t.place(x=x2[i], y=y2)
    l2Arr.append(t)


def createMemoryTable():
  global tMem
  # Memory Table
  titleMem = tk.Label(root)
  titleMem.config(bg=bgColor, text='Memoria Principal')
  titleMem.place(x=570, y=330)

  tMem = Table(root, 17, 3)
  tMem.createTable(titlesMem, '#5696fc', 'white', False)
  tMem.place(x=520, y=350)


def main():
  global tMem, l1Arr, l2Arr, pArr
  queueArr = []

  createProcessorLabel()
  createL1Tables()
  createL2Tables()
  createMemoryTable()

  for _ in range(11):
    queueArr.append(queue.Queue())

  # Processor Labels Events
  root.bind('<<P0CH0>>', lambda e: processProcessorLabel(
      queueArr[2], e, pArr[0]))

  root.bind('<<P1CH0>>', lambda e: processProcessorLabel(
      queueArr[4], e, pArr[1]))

  root.bind('<<P0CH1>>', lambda e: processProcessorLabel(
      queueArr[7], e, pArr[2]))

  root.bind('<<P1CH1>>', lambda e: processProcessorLabel(
      queueArr[9], e, pArr[3]))

  # L1 Tables Events
  root.bind('<<L1CH0P0>>', lambda e: processL1Tables(
      queueArr[3], e, l1Arr[0]))

  root.bind('<<L1CH0P1>>', lambda e: processL1Tables(
      queueArr[5], e, l1Arr[1]))

  root.bind('<<L1CH1P0>>', lambda e: processL1Tables(
      queueArr[8], e, l1Arr[2]))

  root.bind('<<L1CH1P1>>', lambda e: processL1Tables(
      queueArr[10], e, l1Arr[3]))

  # L2 Tables Events
  root.bind('<<L2CH0>>', lambda e: processL2Tables(
      queueArr[1], e, l2Arr[0]))

  root.bind('<<L2CH1>>', lambda e: processL2Tables(
      queueArr[6], e, l2Arr[1]))

  # Memory Table Event
  root.bind('<<MEM>>', lambda e: processMemTables(
      queueArr[0], e, tMem))

  cpu = CpuSystem(queueArr, root)
  cpu.start()

  root.configure(background=bgColor)
  root.attributes('-zoomed', True)
  root.mainloop()


if __name__ == "__main__":
  main()
