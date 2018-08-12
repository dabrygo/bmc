import pygame
import sys
import textwrap
import time

import Color
import Display
import Encoding

# Changeable Properties
background = Color.Black()
text_color = Color.White()
font_size = 32
font = pygame.font.SysFont('courier', font_size, bold=True)

# Derived Properties
width = 1200
height = 400
screen = Display.Screen.size_and_color(width=width, height=height, color=background)

max_chars = 60
wrapper = textwrap.TextWrapper(max_chars)


verse = 'Paul, a prisoner of Christ Jesus, and Timothy, our brother, To Philemon our dear friend and fellow worker'

encoding = Encoding.Blank.hangman(verse)
encoded = encoding.encoded()
lines = wrapper.wrap(encoded)
for i, line in enumerate(lines):
  x = 0
  y = i * font_size
  textbox = Display.TextBox.default(line, text_color, x, y)
  screen.add(textbox)


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    screen.refresh()

