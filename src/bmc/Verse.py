'''Collection of data for a single screen.'''

import abc
import re


class Reference:
  def __init__(self, book, chapter, verse_number):
    self._book = book
    self._chapter = chapter
    self._verse_number = verse_number

  @classmethod
  def from_string(cls, string):
    pattern = r'((\w+ ){1,3})(\d+):(\d+)'
    match = re.search(pattern, string)
    if match is None:
      raise ValueError(f"Invalid reference string: {string}")
    book = match.group(1).strip()
    chapter = int(match.group(3))
    verse = int(match.group(4))
    return cls(book, chapter, verse)

  def __str__(self):
    return f"{self._book} {self._chapter}:{self._verse_number}"

  def __eq__(self, other):
    return str(self) == str(other)

  def __lt__(self, other):
    if self._book != other._book:
      raise NotImplementedError("Book comparison not yet implemented")
    if self._chapter < other._chapter:
      return True
    if self._chapter > other._chapter:
      return False
    return self._verse_number < other._verse_number


class Verse:
  def __eq__(self, other):
    return self.reference() == other.reference() \
      and self.section()==other.section() \
      and self.text()==other.text()

  def __lt__(self, other):
    return self.reference() < other.reference()

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
    ref_str = self._verse().group(1)
    self._reference = Reference.from_string(ref_str)
 
  def __eq__(self, other):
    return self._reference == other._reference

  def __lt__(self, other):
    return self._reference < other._reference

  @classmethod
  def from_string(cls, string):
    parts = string.split("|")
    reference = parts[0].strip()
    section = parts[1].strip()
    text = parts[2].strip()
    return cls(section=section, text=f'{reference} {text}')

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
    return str(self._reference)

  def section(self):
    return self._section

  def text(self):
    return self._verse().group(3)

  def lines(self):
    return self.text()
