'''A collection of words for a user to guess'''

import abc
import re

import Tokens
import Word


class Sample(abc.ABC):
  @abc.abstractmethod
  def text(self):
    pass

  @abc.abstractmethod
  def guess(self, guess):
    pass

  @abc.abstractmethod
  def hint(self):
    pass

  @abc.abstractmethod
  def shift(self):
    pass

  @abc.abstractmethod
  def key(self):
    pass

  @abc.abstractmethod
  def guessable(self):
    pass


class Classic(Sample):
  def __init__(self, tokens):
    self._tokens = tokens

  def _current(self):
    for i, token in enumerate(self._tokens):
      if token.guessable():
        return i, token
    raise Exception("No guessable tokens found")

  def text(self):
    statuses = [token.status() for token in self._tokens]
    return ''.join(statuses)

  def shift(self):
    tokens = self._tokens()
    index = self._index
    n = len(tokens)
    for i in range(index+1, n): 
      token = tokens[i]
      if not isinstance(token, Word.Ignore):
        self._index = i
        return
    raise Exception("No next token found")

  def hint(self):
    index, current = self._current()
    current.hint()
    self._tokens[index] = current

  def guess(self, guess):
    index, current = self._current()
    self._tokens[index] = Word.Ignore(current.guess(guess))

  def key(self):
    _, current = self._current()
    return current.key()

  def guessable(self):
    try:
      _, current = self._current()
      return current.guessable()
    except Exception:
      return False
