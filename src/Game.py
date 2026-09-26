'''Play a game.'''

import sys
import time

import pygame

import Display
import GameMode


# FIXME Belongs in Settings Maker
HINT_KEY = pygame.K_SLASH
delay = 0.25  # seconds to wait before changing a screen

# In Mode 1 User must reveal N words to go to next screen
N_WORDS_MODE_1 = 5 


class Game:
  def __init__(self, model, view, verses, mode):
    self._model = model
    self._view = view
    self._verses = verses
    self._mode = mode

  def _game_mode(self, mode, verse):
    attempts = self._model.attempts()
    if mode == 1:
      return GameMode.RandomWord(verse, attempts=attempts, n_words=N_WORDS_MODE_1)
    elif mode == 4:
      return GameMode.AllBlank(verse, attempts=attempts)
    elif mode in [2, 3]:
      raise NotImplemented(f"Game mode {mode} not implemented")
    else:
      raise ValueError(f"Unsupported game mode {mode}")

  def handle_clock_tick(self):
    self._model.clock_ticked()
    self._view.update_score_bar()

  def handle_correct(self, verse, mode):
    self._model.guess_right()
    self._view.update_score_bar()
    text = mode.on_correct_guess()
    self._view.update_content(text, verse=verse)

  def handle_hint(self, verse, mode):
    self._model.request_hint()
    self._view.update_score_bar()
    text = mode.on_hint()
    self._view.update_content(text, verse=verse)

  def handle_incorrect(self, verse, mode):
    self._model.guess_wrong()
    self._view.update_score_bar()
    text = mode.on_incorrect_guess()
    self._view.update_content(text, verse=verse)

  def handle_exit_end_screen(self):
    user_exit = False
    while not user_exit:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYDOWN:
            user_exit = True

  def play(self):
    for verse in self._verses:
      mode = self._game_mode(self._mode, verse)
      content = mode.content()
      self._view.update_content(
        raw_text=content, verse=verse
      )
      
      while mode.must_guess_again():
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            sys.exit()

          if event.type == Display.TIMER_EVENT:
            self.handle_clock_tick()

          if event.type == pygame.KEYDOWN:
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

            self._view.process_events(event)

        self._view.refresh_screen()

      time.sleep(delay)

    self._model.save_to_file()
    self._view.display_end_screen()
    self.handle_exit_end_screen()

