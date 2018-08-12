'''Obscures text'''
import abc
import re

class Encoding(abc.ABC):
  def __init__(self, text):
    self.text = text

  @abc.abstractmethod
  def tokens(self):
    pass 

  @abc.abstractmethod
  def encoded(self):
    pass
    

class Blank(Encoding):
  def __init__(self, text, character):
    self._text = text
    self._character = character
 
  @classmethod
  def hangman(cls, text):
    return cls(text, character='_')

  def tokens(self):
    matches = self._matches()
    tokens = [match.group(0) for match in matches]
    return tokens

  def _matches(self):
    regex = r'\w+'
    return re.finditer(regex, self._text) 

  def encoded(self):
    start = 0
    obscured = ""
    for match in self._matches():
      end = match.start()
      unhideable = self._text[start:end]
      start = match.end()
      hideable = self._character * (start - end)
      obscured = obscured + unhideable + hideable
    return obscured
