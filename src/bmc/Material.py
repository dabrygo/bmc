import os

from bmc import Verse


class Book:
  def __init__(self, lines):
    self._lines = lines 

  @classmethod
  def from_name(cls, book_name):
    directory = 'rsc/books'
    filename = book_name + '.txt'
    path = os.path.join(directory, filename)
    lines = Book._read(path)
    return cls(lines)
  
  @staticmethod
  def _read(file):
    if not os.path.exists(file):
      raise FileNotFoundError(f"Book file not found: {file}")
    with open(file) as f:
      lines = f.readlines()
    return lines

  def parse(self):
    return [Verse.Default.from_string(x) for x in self._lines]
