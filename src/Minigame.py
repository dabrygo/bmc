'''Determines how to complete a screen in a game.'''

import abc
import random

import pygame

import Sample
import Tokens
import Word

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


class Minigame:
  '''An abstract way of playing the game.'''

  def __init__(self, verse):
    self._verse = verse
    text = self._verse.text()
    self._tokens = Tokens.NoBlanking(text)
    self._tokenized = self._tokens.tokenize()
    self._sample = Sample.Classic(self._tokenized)

  def on_same_screen(self):
    '''Returns `false` when time to change to next screen.'''
    return self.must_guess_again()

  def content(self):
    '''What to print to screen.'''
    return self._sample.text()

  def must_guess_again(self):
    '''Returns `true` if user should guess again.'''
    return self._sample.guessable()

  def expected_input(self):
    '''What user should guess to proceed.''' 
    return self._sample.key()

  def _random_indices(self, tokens, k):
    '''Choose `k` random guessable tokens.'''
    blankable = []
    for i, token in enumerate(tokens):
      if not isinstance(token, Word.Ignore):
        blankable.append(i)

    return random.sample(blankable, k=k)

  def _random_phrase_indices(self, tokens, k, length):
    '''Choose `k` random guessable tokens in groups of `length`.'''
    blankable = []
    for i, token in enumerate(tokens):
      if not isinstance(token, Word.Ignore):
        blankable.append(i)

    # Find phrases
    n = len(blankable)
    phrases = []
    for i in range(0, n, length):
      phrase = blankable[i:i+length]
      is_valid_phrase = len(phrase) == length
      if is_valid_phrase:
        phrases.append(phrase)

    # Choose phrases
    assert(len(phrases) >= k)
    random_phrases = random.sample(phrases, k) 

    # Flatten
    result = [i for phrase in random_phrases for i in phrase]

    return result

  def _hide_words_at_indices(self, indices):
    '''Blank the tokens at the given indices.'''
    new_tokens = []
    for i, token in enumerate(self._tokenized):
      if i in indices:
        token.hide()
        new_tokens.append(token)
      else:
        token.show()
        new_tokens.append(token)
    self._tokenized = new_tokens
    self._sample = Sample.Classic(self._tokenized)

  @abc.abstractmethod
  def prepare_screen_for_play(self):
    '''What screen looks like on startup, blank-wise.'''
    pass

  def on_hint(self):
    '''What happens when user requests a hint.'''
    self._sample.hint()
    return self._sample.text()

  def on_incorrect_guess(self):
    '''What happens when user guesses incorrectly.'''
    return self._sample.text()

  def on_correct_guess(self):
    '''What happens when user guesses correctly.'''
    key = self._sample.key()
    letter = letters[key]
    self._sample.guess(letter)
    text = self._sample.text()
    return text


class BlankOneWord(Minigame):
  '''User guesses one randomly selected word at a time.'''
  def __init__(self, verse, n_words):
    super().__init__(verse)
    self._n_words = n_words # How many words user must reveal
    self._i_words = 0 # How many words user has revealed
    self._hide_indices = super()._random_indices(
      self._tokenized, k=self._n_words,
    )

  def prepare_screen_for_play(self):
    '''Set up next screen for gameplay.'''
    self._hide_next_word()
 
  def _hide_next_word(self):
    '''Hide a random word from the screen.'''
    i_hide = self._hide_indices[self._i_words]
    super()._hide_words_at_indices([i_hide])

  def _more_words_to_do(self):
    '''Check if there are more words for this screen.'''
    return self._i_words < self._n_words

  def on_correct_guess(self):
    '''What happens when user guesses correctly.'''
    # FIXME Duplicating super() code here a little messy
    key = self._sample.key()
    letter = letters[key]
    self._sample.guess(letter)
    self._i_words += 1
    if self._more_words_to_do():
      self._hide_next_word() 
    return self._sample.text()


class BlankMultipleWords(Minigame):
  '''User iteratively guesses multiple randomly blanked words.'''
  def __init__(self, verse, n_words):
    super().__init__(verse)
    self._tokenized = self._tokens.tokenize()
    self._n_words = n_words # How many words user must reveal

  def prepare_screen_for_play(self):
    '''Set up next screen for gameplay.'''
    i_hide = super()._random_indices(
      self._tokenized, k=self._n_words
    )
    super()._hide_words_at_indices(i_hide)


class BlankPhrases(Minigame):
  '''User iteratively guesses randomly blanked phrases.'''
  def __init__(self, verse, n_phrases, words_per_phrase=3):
    super().__init__(verse)
    self._tokenized = self._tokens.tokenize()
    self._n_phrases = n_phrases # How many words user must reveal
    self._words_per_phrase = words_per_phrase

  def prepare_screen_for_play(self):
    '''Set up next screen for gameplay.'''
    phrase_length = self._words_per_phrase
    if phrase_length <= 1:
      raise ValueError(f"Phrases must have more than one word, found '{phrase_length}'.")
    i_hide = super()._random_phrase_indices(
      self._tokenized,
      k=self._n_phrases,
      length=self._words_per_phrase,
    )
    super()._hide_words_at_indices(i_hide)


class BlankAllWords(Minigame):
  '''User guesses all words.'''
  def __init__(self, verse):
    super().__init__(verse)

  def prepare_screen_for_play(self):
    '''Set up next screen for gameplay.'''
    tokens = self._tokens.tokenize()
    for word in tokens:
      word.hide()
    self._sample = Sample.Classic(tokens)

