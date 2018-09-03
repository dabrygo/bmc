import abc

import Pattern
import Verse

class Reader:
  '''A supplier of lines of text'''
  @abc.abstractmethod
  def lines(self):
    pass


def Fake(Reader):
  def __init__(self, lines):
    self._lines = lines

  def lines(self):
    return self._lines


def File(Reader):
  def __init__(self, filename):
    self._filename = filename

  def lines(self, max_width):
    with open(self._filename) as f:
      return f.readlines()

