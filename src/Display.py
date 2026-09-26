'''Present game to user.'''

import sys
import textwrap
import time

import pygame
import pygame_gui

import GameData
import GameMode

# TODO Where to put init() code?
pygame.init()

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 400

N_CONTENT_LINES = 8
CONTENT_WIDTH = 600

TIMER_EVENT = pygame.USEREVENT + 1 # Define a unique custom event ID
MS_PER_SECOND = 1000

# FIXME Belongs in Settings Maker
HINT_KEY = pygame.K_SLASH
delay = 0.25  # seconds to wait before changing a screen

# FIXME Belongs in Game Rules
GAME_MODE = 1
MAX_ATTEMPTS = 3
# In Mode 1 User must reveal N words to go to next screen
N_WORDS_MODE_1 = 5 

# Derived properties
#n_cols = 120
#n_rows = 30
#avg_char_height = ((.7 + 1.0) / 2) * font_size
#avg_char_width = .6 * font_size
#width = n_cols * avg_char_width
#height = n_rows * avg_char_height

max_chars = 60
wrapper = textwrap.TextWrapper(max_chars)

font_size = 24
font_face = 'Consolas'
font_path = "c:/windows/fonts/consolas.ttf"
font = pygame.font.SysFont(font_face, size=font_size)

def htmlify(text):
  return f'<font face="consolas">' + text + '</span>'


class ContentBox:
  '''A text box that contains game content (as opposed to score)'''
  def __init__(self, manager, label, position, size, text):
    self._gui_element = pygame_gui.elements.UITextBox(
        html_text=htmlify(text),
        relative_rect=pygame.Rect(position, size),
        manager=manager,
        object_id=pygame_gui.core.ObjectID(
            class_id='@new_text_box',
            object_id=f'#new_text_box_{label.lower()}'
        )
    )

  def set_text(self, text):
    self._gui_element.set_text(htmlify(text))


class ScoreBox:
    BOX_SIZE = 100

    def __init__(self, manager, label, position, tally):
      self._label = label
      self._tally = tally
      self._position = position
      self._gui_element = pygame_gui.elements.UITextBox(
        html_text=self._text(),
        relative_rect=pygame.Rect(
            self._position,
            (ScoreBox.BOX_SIZE, ScoreBox.BOX_SIZE)
        ),
        manager=manager,
        object_id=pygame_gui.core.ObjectID(
            class_id='@score_box',
            object_id=f'#score_box_{self._label.lower()}'
        )
      )

    def _text(self):
      label = self._label.title()
      count = self._tally.value()
      return htmlify(f"{label}\n{count:05d}")

    def update(self):
      text = self._text()
      self._gui_element.set_text(text)


class ScoreBar:
  def __init__(self, manager, game):
    self._correct = ScoreBox(manager, "Correct", (0 * ScoreBox.BOX_SIZE, 0), game.correct())
    self._incorrect = ScoreBox(manager, "Incorrect", (1 * ScoreBox.BOX_SIZE, 0), game.incorrect())
    self._hints = ScoreBox(manager, "Hints", (2 * ScoreBox.BOX_SIZE, 0), game.hints())
    self._timer = ScoreBox(manager, "Timer", (3 * ScoreBox.BOX_SIZE, 0), game.timer())
    self._total = ScoreBox(manager, "Score", (4 * ScoreBox.BOX_SIZE, 0), game.total())
    self._attempts = ScoreBox(manager, "Attempts", (5 * ScoreBox.BOX_SIZE, 0), game.attempts())

  def update(self):
    self._total.update()
    self._correct.update()
    self._incorrect.update()
    self._hints.update()
    self._timer.update()
    self._attempts.update()


class GameScreen:
  def __init__(self, width=800, height=400):
    self._screen = pygame.display.set_mode((width, height))

    self._manager = pygame_gui.UIManager(
        (width, height), 
        theme_path="rsc/bmc_default_theme.json",
    )
    self._manager.add_font_paths(font_face, font_path)

    self._game = GameData.Session(GAME_MODE, MAX_ATTEMPTS)

    self._score_bar = ScoreBar(self._manager, self._game)

    self._content_text_boxes = [None for i in range(N_CONTENT_LINES)]
    self._draw_content_boxes()

    # Set the timer to trigger every second 
    self._clock = pygame.time.Clock()
    pygame.time.set_timer(TIMER_EVENT, millis=MS_PER_SECOND) 

  def _draw_content_boxes(self):
    box_height = font_size + 10
    for i in range(N_CONTENT_LINES):
      x = 0 
      y = ScoreBox.BOX_SIZE + i * box_height 
      text_box = ContentBox(
        manager=self._manager, 
        label=f"verse_{i}",
        position=(x, y), 
        size=(CONTENT_WIDTH, box_height), 
        text=""
      )
      self._content_text_boxes[i] = text_box

  def update_score_bar(self):
    self._score_bar.update()

  def update_content(self, raw_text, verse=None):
    # Wrap text to fit on screen
    wrapped = wrapper.wrap(raw_text)
    if verse:
      section = verse.section()
      wrapped.insert(0, section)
      reference = verse.reference()
      wrapped.insert(1, reference)
    assert len(wrapped) <= N_CONTENT_LINES

    for i in range(N_CONTENT_LINES):
      text_box = self._content_text_boxes[i]
      if i < len(wrapped):
        line = wrapped[i]
      else:
        line = ""
      text_box.set_text(line)

  def refresh_screen(self):
    time_delta = self._clock.tick(60) / MS_PER_SECOND
    self._manager.update(time_delta)
    self._manager.draw_ui(self._screen)
    pygame.display.update()

  def game_mode(self, mode):
    if mode == 1:
      return GameMode.RandomWord
    elif mode == 4:
      return GameMode.AllBlank
    elif mode in [2, 3]:
      raise NotImplemented(f"Game mode {mode} not implemented")
    else:
      raise ValueError(f"Unsupported game mode {mode}")

  def handle_clock_tick(self):
    self._game.clock_ticked()
    self.update_score_bar()

  def handle_correct(self, verse, mode):
    self._game.guess_right()
    self.update_score_bar()
    text = mode.on_correct_guess()
    self.update_content(text, verse=verse)

  def handle_hint(self, verse, mode):
    self._game.request_hint()
    self.update_score_bar()
    text = mode.on_hint()
    self.update_content(text, verse=verse)

  def handle_incorrect(self, verse, mode):
    self._game.guess_wrong()
    self.update_score_bar()
    text = mode.on_incorrect_guess()
    self.update_content(text, verse=verse)

  def run(self, verses):
    mode_type = self.game_mode(GAME_MODE)
    for verse in verses:
      attempts = self._game.attempts()
      # FIXME Don't check GAME MODE more than once
      if GAME_MODE == 1:
        mode = mode_type(verse, attempts=attempts, n_words=N_WORDS_MODE_1)
      else:
        mode = mode_type(verse, attempts=attempts)

      content = mode.content()
      self.update_content(raw_text=content, verse=verse)
      
      while mode.must_guess_again():
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            sys.exit()

          if event.type == TIMER_EVENT:
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

            self._manager.process_events(event)

        self.refresh_screen()

      time.sleep(delay)

    text = 'Press any key to exit'
    self.update_content(text)
    self.refresh_screen()
    user_exit = False
    while not user_exit:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYDOWN:
            user_exit = True

    self._game.save_to_file()
