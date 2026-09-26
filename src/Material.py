import os

import Parser
import Reader


class Book:
  def __init__(self, book_name):
    # TODO Clean up __init__
    directory = 'rsc/books'
    filename = book_name + '.txt'
    path = os.path.join(directory, filename)
    reader = Reader.File(path)
    lines = reader.lines()
    parser = Parser.Simple(lines)
    self._verses = parser.parse()

  def verses(self):
    return self._verses
