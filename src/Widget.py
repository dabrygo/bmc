import pygame


BLACK = (255, 255, 255)
BLUE = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)


class TextPane:
  def __init__(self, draw_surface, border_color, bkgd_color, text, text_color, text_font):
    self._draw_surface = draw_surface
    self._border_color = border_color
    self._bkgd_color = bkgd_color
    self._text = text
    self._text_font = text_font
    self._text_color = text_color

  @classmethod
  def default_font(cls, draw_surface, border_color, bkgd_color, text, font_size, color):
    font = pygame.font.SysFont('consolas', size=font_size)
    return cls(
      draw_surface, border_color, bkgd_color, text, text_color=color, text_font=font
    )

  def surface(self):
    antialias = True
    return self._text_font.render(
      self._text, antialias, self._text_color
    )

  def rectangle(self):
    surface = self.surface()
    return surface.get_rect()

  def set_text(self, text):
    self._text = text
    self.update()

  def update(self):
    surface = self.surface()
    rectangle = surface.get_rect()
    pad = 100
    pad_rectangle = pygame.rect.Rect(
      rectangle.x, rectangle.y, rectangle.width + 2 * pad, rectangle.height + 2 * pad
    )
    border_width = 10
    border_rectangle = pygame.rect.Rect(
      pad_rectangle.x, pad_rectangle.y, pad_rectangle.width + 2 * border_width, pad_rectangle.height + 2 * border_width
    )

    # apply background color
    pygame.draw.rect(self._draw_surface, self._border_color, border_rectangle) 
    pad_rectangle = pad_rectangle.move(pad_rectangle.x + border_width, pad_rectangle.y + border_width)
    pygame.draw.rect(self._draw_surface, self._bkgd_color, pad_rectangle) 
    rectangle = rectangle.move(rectangle.x + border_width, rectangle.y + border_width)
    rectangle = rectangle.move(rectangle.x + pad, rectangle.y + pad)
    pygame.draw.rect(self._draw_surface, self._bkgd_color, rectangle) 
    self._draw_surface.blit(surface, rectangle)
    pygame.display.flip()


class Window:
  def __init__(self, *, title, color, width, height):
    pygame.display.set_caption(title)
    self._screen = pygame.display.set_mode((width, height))
    self._screen.fill(color)
    pygame.display.flip()

  def run(self):
    text_pane = TextPane.default_font(
      self._screen, PURPLE, BLUE, text="Hello, World!", font_size=32, color=RED,
    )
    #border = Border(self._screen, text_pane, color=BLACK, pad=5, width=1)
    text_pane.update()

    run = True
    while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        if event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_b]:
              text_pane.set_text("You pressed the 'b' key!")
            else:
              run = False
    pygame.quit()


pygame.init()

window = Window(title="Test", color=BLACK, width=800, height=600)
window.run()
