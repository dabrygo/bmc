'''Present game to user.'''

import textwrap

import pygame
import pygame_gui


# TODO Where to put init() code?
pygame.init()

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 400

N_CONTENT_LINES = 8
CONTENT_WIDTH = 700

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
    self._attempts = ScoreBox(manager, "Attempts", (0 * ScoreBox.BOX_SIZE, 0), game.attempts())
    self._correct = ScoreBox(manager, "Correct", (1 * ScoreBox.BOX_SIZE, 0), game.correct())
    self._incorrect = ScoreBox(manager, "Incorrect", (2 * ScoreBox.BOX_SIZE, 0), game.incorrect())
    self._hints = ScoreBox(manager, "Hints", (3 * ScoreBox.BOX_SIZE, 0), game.hints())
    self._timer = ScoreBox(manager, "Timer", (4 * ScoreBox.BOX_SIZE, 0), game.timer())
    self._total = ScoreBox(manager, "Score", (5 * ScoreBox.BOX_SIZE, 0), game.total())

  def update(self):
    self._attempts.update()
    self._correct.update()
    self._incorrect.update()
    self._hints.update()
    self._timer.update()
    self._total.update()


class Screen:
  def __init__(self, width=800, height=400):
    size = (width, height)
    self._screen = pygame.display.set_mode(size)

    self._manager = pygame_gui.UIManager(
        size,
        theme_path="rsc/bmc_default_theme.json",
    )
    self._manager.add_font_paths(font_face, font_path)

    # Set the timer to trigger every second 
    self._clock = pygame.time.Clock()
    pygame.time.set_timer(TIMER_EVENT, millis=MS_PER_SECOND) 

  def _draw_content_boxes(self, n_boxes, x_start, y_start):
    box_height = font_size + 10
    for i in range(n_boxes):
      x = x_start 
      y = y_start + i * box_height 
      text_box = ContentBox(
        manager=self._manager, 
        label=f"verse_{i}",
        position=(x, y), 
        size=(CONTENT_WIDTH, box_height), 
        text=""
      )
      self._content_text_boxes[i] = text_box

  def process_events(self, event):
    self._manager.process_events(event)

  def refresh_screen(self):
    time_delta = self._clock.tick(60) / MS_PER_SECOND
    self._manager.update(time_delta)
    self._manager.draw_ui(self._screen)
    pygame.display.update()

  def update_content(self, raw_text, n_boxes=N_CONTENT_LINES, verse=None):
    # Wrap text to fit on screen
    wrapped = wrapper.wrap(raw_text)
    if verse:
      section = verse.section()
      wrapped.insert(0, section)
      reference = verse.reference()
      wrapped.insert(1, reference)
    assert len(wrapped) <= n_boxes 

    for i in range(n_boxes):
      text_box = self._content_text_boxes[i]
      if i < len(wrapped):
        line = wrapped[i]
      else:
        line = ""
      text_box.set_text(line)



class SelectMinigame(Screen):
  '''Screen for selecting what kind of game to play.'''

  def __init__(self, width=800, height=500):
    super().__init__(width, height)

    self._minigames = [
      (
        0, 
        "Minigames test different recall skills. Enter a game code via keyboard to choose it.", 
        'Examples underneath mode for reference.'
      ),
      (
        1,
        'Blank One Word',
        'I have hidden your ____ in my heart that I might not sin against you.'
      ),
      (
        2,
        'Blank Multiple Words',
        'I have ______ ____ word in my heart ____ I might not sin _______ you.'
      ),
      (
        3,
        'Blank Phrases',
        '_ ____ ______ your ____ __ __ heart that I might not ___ _______ ___.'
      ),
      (
        4,
        'Blank All',
         '_ ____ ______ ____ ____ __ __ _____ ____ _ _____ ___ ___ _______ ___.'
      ),
    ]
    n_minigames = len(self._minigames)
    self._n_boxes = 2 * n_minigames
    self._content_text_boxes = [None for _ in range(self._n_boxes)]
    self._draw_content_boxes(
      n_boxes=self._n_boxes, x_start=0, y_start=ScoreBox.BOX_SIZE
    )
    self.update_content()

  def update_content(self):
    # Wrap text to fit on screen
    for i, item in enumerate(self._minigames):
      code, label, example = item
      text_box = self._content_text_boxes[2*i]
      if code == 0:
        line = f'{label}'
      else:
        line = f'{code}. {label}'

      text_box.set_text(line)

      text_box = self._content_text_boxes[2*i+1]
      line = f'        {example}'
      text_box.set_text(line)


class GameScreen(Screen):
  '''A window for the user to play a game on.'''

  def __init__(self, game_data, width=800, height=400):
    super().__init__(width, height)

    self._score_bar = ScoreBar(self._manager, game_data)

    self._content_text_boxes = [None for _ in range(N_CONTENT_LINES)]
    self._draw_content_boxes(
      n_boxes=N_CONTENT_LINES, x_start=0, y_start=ScoreBox.BOX_SIZE
    )

  def update_score_bar(self):
    self._score_bar.update()

  def display_end_screen(self):
    text = 'Press ESC to exit or any other key to keep playing'
    self.update_content(text)
    self.refresh_screen()
