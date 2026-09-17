'''Present game to user.'''

import abc

import pygame
import pygame_gui

pygame.init()

# TODO Do we need to call init() for text? 
class Text:
  def __init__(self, font, text, color):
    self._font = font
    self._text = text
    self._color = color

  def surface(self):
    rgb = self._color.rgb()
    return self._font.render(self._text, True, rgb)


class Box:
  def __init__(self, x, y, width, height):
    self._x = x
    self._y = y
    self._width = width
    self._height = height

  def rectangle(self):
    return pygame.rect.Rect(self._x, self._y, self._width, self._height)


# TODO Use ABC on Blittable and make TextBox a subclass
class BlittableText(abc.ABC):
  @abc.abstractmethod
  def surface(self):
    pass

  @abc.abstractmethod
  def rectangle(self):
    pass


class TextBox(BlittableText):
  def __init__(self, surface, rectangle):
    self._surface = surface
    self._rectangle = rectangle

  @classmethod
  def default(cls, text, color, x, y):
    font_size = 32
    font = pygame.font.SysFont('courier', font_size, bold=True)
    return TextBox.default_modified(cls, text, font, color, x, y)

  @classmethod
  def default_modified(cls, text, font, color, x, y):
    text = Text(font, text, color)
    surface = text.surface()
    surface_rectangle = surface.get_rect()
    width = surface_rectangle.width
    height = surface_rectangle.height
    rectangle = pygame.rect.Rect(x, y, width, height)
    return cls(surface, rectangle)

  def surface(self):
    return self._surface

  def rectangle(self):
    return self._rectangle



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


class ScoreBox:
    BOX_SIZE = 100

    def __init__(self, manager, label, increment_rule, position):
        self._label = label
        self._tally = 0
        self._increment_rule = increment_rule
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
        return f"{self._label.title()}\n{self._tally:05d}"

    def increment(self):
      self.set_tally(self._tally + 1)

    def set_tally(self, tally):
      self._tally = tally
      text = self._text()
      self._gui_element.set_text(text)

