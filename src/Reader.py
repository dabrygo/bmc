import abc

import Pattern
import Verse

class Reader:
  '''A supplier of lines of text'''
  @abc.abstractmethod
  def lines(self):
    pass


class Fake(Reader):
  def __init__(self, lines):
    self._lines = lines

  def lines(self):
    return self._lines


class File(Reader):
  def __init__(self, filename):
    self._filename = filename

  def lines(self):
    with open(self._filename) as f:
      return f.readlines()

