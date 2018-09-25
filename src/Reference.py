import abc
import re

class Reference(abc.ABC):
  def __str__(self):
    return f'{self.book()} {self.chapter()}:{self.verse()}'

  @abc.abstractmethod
  def book(self):
    pass

  @abc.abstractmethod
  def chapter(self):
    pass

  @abc.abstractmethod
  def verse(self):
    pass


class Fields(Reference):
  def __init__(self, book, chapter, verse):
    self._book = book
    self._chapter = chapter
    self._verse = verse

  def book(self):
    return self._book

  def chapter(self):
    return self._chapter

  def verse(self):
    return self._verse


class Standard(Reference):
  def __init__(self, string):
    self._string = string

  def _match(self):
    return re.search(r'((\d )?(\w+ )+)(\d+):(\d+)', self._string)

  def book(self):
    match = self._match()
    name = match.group(1)
    return name.strip()

  def chapter(self):
    match = self._match()
    return int(match.group(4))

  def verse(self):
    match = self._match()
    return int(match.group(5))
