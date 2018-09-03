import abc

import Pattern
import Verse

class Parser:
  @abc.abstractmethod
  def parse(self, max_width):
    pass


class Simple(Parser):
  def __init__(self, lines):
    self._lines = lines

  def parse(self, max_width):
    verses = []
    section = ""
    for line in self._lines:
      pattern = Pattern.Verse(line)
      if not pattern.matches():
        section = line.rstrip()
      else:
        verse = Verse.Default(section, line, max_width) 
        verses.append(verse)
    return verses

