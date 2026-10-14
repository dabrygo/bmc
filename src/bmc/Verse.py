'''Collection of data for a single screen.'''

import abc
import re


class Verse:
  def __eq__(self, other):
    return self.reference() == other.reference() \
      and self.section()==other.section() \
      and self.text()==other.text()

  @abc.abstractmethod
  def within(self, string):
    '''Returns `true` if a verse can be found in the given string.'''
    pass

  @abc.abstractmethod
  def reference(self):
    '''Unique identifier for this verse.'''
    pass

  @abc.abstractmethod
  def section(self):
    '''Contextual description of this verse and other verses near it.'''
    pass

  @abc.abstractmethod
  def text(self):
    '''Plain text of this verse.'''
    pass

  @abc.abstractmethod
  def lines(self):
    '''Text of this verse as it appears originally. (Preserves whitespace, e.g.)'''
    pass


class Fake(Verse):
  def __init__(self, section, reference, text):
    self._reference = reference
    self._section = section
    self._text = text

  def within(self, string):
    '''Returns `true` if a verse can be found in the given string.'''
    pass

  def reference(self):
    return self._reference

  def section(self):
    return self._section

  def text(self):
    return self._text

  def lines(self):
    raise NotImplementedError("Not yet implemented")


class Default(Verse):
  def __init__(self, section, text):
    self._section = section
    self._text = text

  @staticmethod
  def _find(string):
    pattern = r'((\w+ ){1,3}\d+:\d+) (.+)'
    return re.search(pattern, string)

  @staticmethod
  def within(string):
    '''Returns `true` if a verse can be found in the given string.'''
    return Default._find(string) is not None

  def _verse(self):
    return Default._find(self._text)
 
  def reference(self):
     return self._verse().group(1)

  def section(self):
    return self._section

  def text(self):
    return self._verse().group(3)

  def lines(self):
    return self.text()
