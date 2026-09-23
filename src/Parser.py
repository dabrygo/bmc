'''Converts raw data (e.g., from input files) to objects'''

import abc

import Pattern
import Verse


class Parser:
  @abc.abstractmethod
  def parse(self, max_width):
    pass


class Simple(Parser):
  '''Reads a new verse from each distinct string'''

  def __init__(self, lines):
    self._lines = lines

  def parse(self):
    verses = []
    section = ""
    for line in self._lines:
      pattern = Pattern.Verse(line)
      if not pattern.matches():
        section = line.rstrip()
      else:
        verse = Verse.Default(section, line) 
        verses.append(verse)
    return verses

