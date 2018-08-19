import abc
import re
import textwrap

import Pattern


class Verse:
  @abc.abstractmethod
  def reference(self):
    pass

  @abc.abstractmethod
  def section(self):
    pass

  @abc.abstractmethod
  def text(self):
    pass

  @abc.abstractmethod
  def lines(self):
    pass


class Default(Verse):
  def __init__(self, section, text, max_width):
    self._section = section
    self._text = text
    self._max_width = max_width

  def _pattern(self):
    return Pattern.Verse(self._text)
 
  def reference(self):
     pattern = self._pattern()
     return pattern.group(1)

  def section(self):
    return self._section

  def text(self):
    pattern = self._pattern()
    return pattern.group(2)

  def lines(self):
    text = self.text()
    wrapper = textwrap.TextWrapper(self._max_width)
    return wrapper.wrap(text)


class Blanked(Verse):
  def __init__(self, verse, encoding):
    self._verse = verse 
    self._encoding = encoding

  def reference(self):
    pass

  def section(self):
    pass

  def text(self):
    return self._encoding.encoded()

  def lines(self):
    return self._verse.lines()



