'''Play a game.'''

import sys
import time

import pygame

import Display
import GameMode


# Basic Game Logic:
# User guesses right
#   If no more words, change screen
# User requests hint
#   If reveals word, count as a wrong or a hint?
# User guesses wrong
#   If user has more attempts, stay on current word
#   Count as a wrong or as an attempt?
#     If count as wrong, multiply by number of bad attempts?
#   If user has no more attempts, move to next word

# FIXME Belongs in Settings Maker
HINT_KEY = pygame.K_SLASH
delay = 0.25  # seconds to wait before changing a screen

# In Modes 1 & 2 user must reveal N words to go to next screen
N_WORDS_PER_SCREEN = 3 

# In Mode 3 user must reveal N phrases with this length
WORDS_PER_PHRASE = 3


class Game:
  def __init__(self, model, view, verses, mode):
    self._model = model
    self._view = view
    self._verses = verses
    self._mode = mode

  def _game_mode(self, mode, verse):
    '''Choose what kind of game to play.'''
    if mode == 1:
      return GameMode.BlankOneWord(
        verse, n_words=N_WORDS_PER_SCREEN,
      )
    elif mode == 2:
       return GameMode.BlankMultipleWords(
        verse, n_words=N_WORDS_PER_SCREEN,
      )
    elif mode == 3:
      return GameMode.BlankPhrases(
        verse,
        n_phrases=N_WORDS_PER_SCREEN,
        words_per_phrase=WORDS_PER_PHRASE,
      )
    elif mode == 4:
      return GameMode.BlankAllWords(verse)
    else:
      raise ValueError(f"Unsupported game mode {mode}")

  def handle_new_screen(self, verse, mode):
    '''Update to a new screen.'''
    mode.prepare_screen_for_play()
    content = mode.content()
    self._view.update_content(
      raw_text=content, verse=verse
    )

  def handle_clock_tick(self):
    '''Do work for when the clock ticks.'''
    self._model.clock_ticked()
    self._view.update_score_bar()

  def handle_correct(self, verse, mode):
    '''Do work for when the user guesses correctly.'''
    self._model.guess_right()
    self._view.update_score_bar()
    text = mode.on_correct_guess()
    self._view.update_content(text, verse=verse)

  def handle_hint(self, verse, mode):
    '''Do work for when the user requests a hint.'''
    self._model.request_hint()
    self._view.update_score_bar()
    text = mode.on_hint()
    self._view.update_content(text, verse=verse)

  def handle_incorrect(self, verse, mode):
    '''Do work for when the user guesses incorrectly.'''
    self._model.guess_wrong()
    self._view.update_score_bar()
    text = mode.on_incorrect_guess()
    self._view.update_content(text, verse=verse)

  def handle_user_input(self, verse, mode):
    '''Handle user input for the current screen.'''

    pressed_keys = pygame.key.get_pressed()

    expected_input = mode.expected_input()
    is_correct = pressed_keys[expected_input]

    is_hint = pressed_keys[HINT_KEY]

    if is_correct:
      self.handle_correct(verse, mode)
    elif is_hint:
      self.handle_hint(verse, mode)
    else: # is_incorrect
      self.handle_incorrect(verse, mode)

  def handle_exit_end_screen(self):
    '''Handle exiting the end screen.'''
    user_exit = False
    while not user_exit:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYDOWN:
            user_exit = True

  def play(self):
    '''Play a game.'''
    for verse in self._verses:
      mode = self._game_mode(self._mode, verse)

      self.handle_new_screen(verse, mode)
      while mode.on_same_screen():
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            sys.exit()

          if event.type == Display.TIMER_EVENT:
            self.handle_clock_tick()

          if event.type == pygame.KEYDOWN:
            self.handle_user_input(verse, mode)

          self._view.process_events(event)

        self._view.refresh_screen()

      time.sleep(delay)

    self._model.save_to_file()
    self._view.display_end_screen()
    self.handle_exit_end_screen()

