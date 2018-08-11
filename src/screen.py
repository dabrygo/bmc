import pygame
import sys
import textwrap
import time

import Color


verse = 'Paul, a prisoner of Christ Jesus, and Timothy, our brother, To Philemon our dear friend and fellow worker'

pygame.init()
pygame.font.init()

font_size = 32
font = pygame.font.SysFont('courier', font_size, bold=True)

max_chars = 60
max_lines = 4

width = max_chars * font_size
height = 400
screen = pygame.display.set_mode((width, height))

background = Color.Black()
text_color = Color.White()


wrapper = textwrap.TextWrapper(max_chars)
lines = wrapper.wrap(verse)
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    screen.fill(background.rgb())

    for i, line in enumerate(lines):
      rect = pygame.rect.Rect(0, i * font_size, width, font_size)
      text = font.render(line, True, text_color.rgb())
      screen.blit(text, rect) 
    pygame.display.update() 

