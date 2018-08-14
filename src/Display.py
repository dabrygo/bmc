import abc

import pygame

import Color


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
  def __init__(self, screen, color, contents=[]):
    self._screen = screen
    self._color = color
    self._contents = contents

  @classmethod
  def size_and_color(cls, width, height, color):
    size = (width, height)
    screen = pygame.display.set_mode(size)
    return cls(screen, color)
 
  def add(self, item):
    self._contents.append(item)

  def refresh(self):
    rgb = self._color.rgb()
    self._screen.fill(rgb)
    for item in self._contents:
      surface = item.surface()
      rectangle = item.rectangle()
      self._screen.blit(surface, rectangle)
    pygame.display.update() 
 
