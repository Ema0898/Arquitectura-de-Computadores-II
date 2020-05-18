import tkinter as tk
from tkinter import Label
import queue
import threading

from chip import Chip


def process(storage, event, label):
  msg = storage.get()
  texto = tk.StringVar()
  texto.set(msg)
  label.config(textvariable=texto)
  print("New message: {0}".format(msg))


def main():
  message_queue = queue.Queue()
  root = tk.Tk()

  lock = threading.Lock()

  chip1 = Chip(0, 2, message_queue, root, lock)
  chip1.startCores()

  chip1 = Chip(1, 2, message_queue, root, lock)
  chip1.startCores()

  label = Label(root)
  label.pack()

  root.bind('<<MessageGenerated>>', lambda e: process(message_queue, e, label))
  root.mainloop()


if __name__ == "__main__":
  main()
