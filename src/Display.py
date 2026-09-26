'''Present game to user.'''

import textwrap

import pygame
import pygame_gui


# TODO Where to put init() code?
pygame.init()

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 400

N_CONTENT_LINES = 8
CONTENT_WIDTH = 600

TIMER_EVENT = pygame.USEREVENT + 1 # Define a unique custom event ID
MS_PER_SECOND = 1000


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
  def __init__(self, game_data, width=800, height=400):
    self._screen = pygame.display.set_mode((width, height))

    self._manager = pygame_gui.UIManager(
        (width, height), 
        theme_path="rsc/bmc_default_theme.json",
    )
    self._manager.add_font_paths(font_face, font_path)

    self._score_bar = ScoreBar(self._manager, game_data)

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

  def process_events(self, event):
    self._manager.process_events(event)

  def refresh_screen(self):
    time_delta = self._clock.tick(60) / MS_PER_SECOND
    self._manager.update(time_delta)
    self._manager.draw_ui(self._screen)
    pygame.display.update()

  def display_end_screen(self):
    text = 'Press any key to exit'
    self.update_content(text)
    self.refresh_screen()
