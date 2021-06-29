import abc
import re

import Word

class Tokens(abc.ABC):
  @abc.abstractmethod
  def tokenize(self):
    pass

class Classic(Tokens):
  def __init__(self, text):
    self._text = text
    self._index = 0

  def tokenize(self):
    words = re.finditer(r"\w+('\w)?", self._text)
    tokens = []
    start = 0
    for match in words:
      ignore_text = self._text[start:match.start()]
      if ignore_text:
        ignore = Word.Ignore(ignore_text)
        tokens.append(ignore)
      word = match.group(0)
      token = Word.Classic(word, character='_')
      tokens.append(token)
      start = match.end()
    ignore_text = self._text[start:]
    if ignore_text:
      ignore = Word.Ignore(ignore_text)
      tokens.append(ignore)
    return tokens

