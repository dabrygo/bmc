'''Determines how to complete a screen in a game.'''

import abc

import pygame

import Sample
import Tokens

letters = {
  pygame.K_a: 'a',
  pygame.K_b: 'b',
  pygame.K_c: 'c',
  pygame.K_d: 'd',
  pygame.K_e: 'e',
  pygame.K_f: 'f',
  pygame.K_g: 'g',
  pygame.K_h: 'h',
  pygame.K_i: 'i',
  pygame.K_j: 'j',
  pygame.K_k: 'k',
  pygame.K_l: 'l',
  pygame.K_m: 'm',
  pygame.K_n: 'n',
  pygame.K_o: 'o',
  pygame.K_p: 'p',
  pygame.K_q: 'q',
  pygame.K_r: 'r',
  pygame.K_s: 's',
  pygame.K_t: 't',
  pygame.K_u: 'u',
  pygame.K_v: 'v',
  pygame.K_w: 'w',
  pygame.K_x: 'x',
  pygame.K_y: 'y',
  pygame.K_z: 'z',
}


class GameMode:
  '''A supplier of lines of text'''
  @abc.abstractmethod
  def content(self):
    '''What to print to screen.'''
    pass

  @abc.abstractmethod
  def must_guess_again(self):
    '''Returns `true` if user should guess again.'''
    pass

  @abc.abstractmethod
  def expected_input(self):
    '''What user should guess to proceed.''' 
    pass

  @abc.abstractmethod
  def on_hint(self):
    '''What happens when user requests a hint.'''
    pass

  @abc.abstractmethod
  def on_correct_guess(self):
    '''What happens when user guesses correctly.'''
    pass

  @abc.abstractmethod
  def on_incorrect_guess(self):
    '''What happens when user guesses incorrectly.'''
    pass



class RandomWord(GameMode):
    '''User guesses randomly selected words one at a time.'''
    def __init__(self, verse):
       self._verse = verse

    def content(self):
      text = self._verse.text()
      tokens = Tokens.Classic(text)
      tokenized = tokens.tokenize()
      sample = Sample.Classic(tokenized)
      lines = sample.text()
      section = self._verse.section()
      lines.insert(0, section)
      reference = self._verse.reference()
      lines.insert(1, reference)
      return lines


class AllBlank:
  '''User guesses all words.'''
  def __init__(self, verse):
    self._verse = verse
    text = self._verse.text()
    tokens = Tokens.Classic(text)
    tokenized = tokens.tokenize()
    self._sample = Sample.Classic(tokenized)
 
  def content(self):
    return self._sample.text()

  def must_guess_again(self):
    return self._sample.guessable()

  def expected_input(self):
    return self._sample.key()

  def on_hint(self):
    self._sample.hint()
    return self._sample.text()

  def on_correct_guess(self):
    key = self._sample.key()
    letter = letters[key]
    self._sample.guess(letter)
    return self._sample.text()

  def on_incorrect_guess(self):
    return self._sample.text()
     