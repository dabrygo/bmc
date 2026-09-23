'''Collection of data for a single screen.'''

import abc

import Pattern


class Verse:
  def __eq__(self, other):
    return self.reference() == other.reference() \
      and self.section()==other.section() \
      and self.text()==other.text()

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
    return self.text()


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
