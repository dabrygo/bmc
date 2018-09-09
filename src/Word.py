'''Base unit that user must uncover before continuing'''

import abc

class Word(abc.ABC):
  '''Base unit that user must uncover before continuing'''
  @abc.abstractmethod
  def status(self):
    '''Text to show to (or hide from) user'''
    pass

  @abc.abstractmethod
  def hint(self):
    '''Determines whether to reveal more of the word'''
    pass

  @abc.abstractmethod
  def guess(self, guess):
    '''Determines whether or not to show the whole word'''
    pass


class Classic(Word):
  '''A blanked word whose hints reveal one letter at the time from the end'''

  def __init__(self, text, character='_'):
    self._text = text
    self._index = len(self._text)
    self._character = character

  def status(self):
    blanked = self._text[:self._index]
    showing = self._text[self._index:]
    blanks = self._character * len(blanked)
    return blanks + showing

  def hint(self):
    if self._index == 0:
      raise Exception("Cannot allow more hints than letters in word")
    self._index -= 1
    return self.status()

  def guess(self, guess):
    guess_lower = guess.lower()
    text_lower = self._text.lower()
    if text_lower.startswith(guess_lower):
      return self._text
    return self.status()
