'''Base unit that user must uncover before continuing'''

import abc
import pygame

letters = {
        'a': pygame.K_a,
        'b': pygame.K_b,
        'c': pygame.K_c,
        'd': pygame.K_d,
        'e': pygame.K_e,
        'f': pygame.K_f, 
        'g': pygame.K_g, 
        'h': pygame.K_h, 
        'i': pygame.K_i, 
        'j': pygame.K_j, 
        'k': pygame.K_k, 
        'l': pygame.K_l, 
        'm': pygame.K_m, 
        'n': pygame.K_n, 
        'o': pygame.K_o, 
        'p': pygame.K_p, 
        'q': pygame.K_q, 
        'r': pygame.K_r, 
        's': pygame.K_s, 
        't': pygame.K_t, 
        'u': pygame.K_u, 
        'v': pygame.K_v, 
        'w': pygame.K_w, 
        'x': pygame.K_x, 
        'y': pygame.K_y, 
        'z': pygame.K_z, 
       }


class Word(abc.ABC):
  '''Base unit that user must uncover before continuing'''

  @abc.abstractmethod
  def hide(self):
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

  @abc.abstractmethod
  def status(self):
    '''The current state of the word'''
    pass

  @abc.abstractmethod
  def matches(self, guess):
    '''Returns true if a guess can reveal a word'''
    pass

  @abc.abstractmethod
  def show(self):
    '''The true form of text'''
    pass

  @abc.abstractmethod
  def guessable(self):
    '''Whether the user can guess about this token'''
    pass

  @abc.abstractmethod
  def key(self):
    '''Input that triggers revealing this word'''
    pass



class Ignore(Word):
  '''A word that does not need to be guessed'''

  def __init__(self, text):
    self._text = text

  def hide(self):
    return self._text

  def status(self):
    return self._text

  def hint(self):
    raise Exception("Cannot provide hints for an ignored word")

  def guess(self, guess):
    raise Exception("Cannot guess on an ignored word")

  def matches(self, guess):
    raise Exception("No match for an ignored word")

  def show(self):
    '''The true form of text'''
    return self._text

  def guessable(self):
    '''A user can never guess on ignored text'''
    return False

  def key(self):
    '''Input that triggers revealing this word'''
    raise Exception("Ignorable word has no key")


class Classic(Word):
  '''A blanked word whose hints reveal one letter at the time from the end'''

  def __init__(self, text, character='_'):
    self._text = text
    self._index = len(self._text)
    self._character = character

  def __str__(self):
    return self.status()

  # FIXME: Update this to follow eval(repr) contract 
  def __repr__(self):
    return self._text
  
  def hide(self):
    return self._character * len(self._text)

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
    if self.matches(guess):
      return self._text
    return self.status()

  def matches(self, guess):
    '''Returns True if a guess is correct'''
    guess_lower = guess.lower()
    text_lower = self._text.lower()
    return text_lower.startswith(guess_lower)

  def show(self):
    '''The true form of text'''
    return self._text

  def guessable(self):
    '''Return False if word is fully shown; True otherwise'''
    return self.status() != self._text

  def key(self):
   letter = self._text[0].lower()
   return letters[letter] 
