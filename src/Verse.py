'''Collection of data for a single screen.'''

import abc
import textwrap

import Pattern


class Verse:
  def __eq__(self, other):
    return self.reference() == other.reference() \
      and self.section()==other.section() \
      and self.text()==other.text()

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


class Fake(Verse):
  def __init__(self, section, reference, text):
    self._reference = reference
    self._section = section
    self._text = text

  def reference(self):
    return self._reference

  def section(self):
    return self._section

  def text(self):
    return self._text

  def lines(self):
    raise NotImplementedError("Not yet implemented")


class Default(Verse):
  def __init__(self, section, text, max_width=None):
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
    return pattern.group(3)

  def lines(self):
    text = self.text()
    if not self._max_width:
      return text
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



