'''Present game to user.'''

import pygame
import pygame_gui

pygame.init()

def htmlify(text):
  return f'<font face="consolas">' + text + '</span>'


class Screen:
  def __init__(self, screen, color):
    self._screen = screen
    self._color = color

  @classmethod
  def size_and_color(cls, width, height, color):
    size = (width, height)
    screen = pygame.display.set_mode(size)
    return cls(screen, color)
 
  def blit(self, items):
    rgb = self._color.rgb()
    self._screen.fill(rgb)
    for item in items:
      surface = item.surface()
      rectangle = item.rectangle()
      self._screen.blit(surface, rectangle)
    pygame.display.update()

  def surface(self):
    return self._screen


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

    def __init__(self, manager, label, position):
        self._label = label
        self._tally = 0
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
        return htmlify(f"{self._label.title()}\n{self._tally:05d}")

    def increment(self):
      self.set_tally(self._tally + 1)

    def set_tally(self, tally):
      self._tally = tally
      text = self._text()
      self._gui_element.set_text(text)

    def tally(self):
      return self._tally
