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


keys = {
        'a': pygame.K_a,
        'b': pygame.K_b,
        'c': pygame.K_c,
        'd': pygame.K_d,
        'e': pygame.K_e,
        'f': pygame.K_f, 
        'g': pygame.K_g, 
        'h': pygame.K_h, 
        'i': pygame.K_i, 
        'j': pygame.K_j, 
        'k': pygame.K_k, 
        'l': pygame.K_l, 
        'm': pygame.K_m, 
        'n': pygame.K_n, 
        'o': pygame.K_o, 
        'p': pygame.K_p, 
        'q': pygame.K_q, 
        'r': pygame.K_r, 
        's': pygame.K_s, 
        't': pygame.K_t, 
        'u': pygame.K_u, 
        'v': pygame.K_v, 
        'w': pygame.K_w, 
        'x': pygame.K_x, 
        'y': pygame.K_y, 
        'z': pygame.K_z, 
       }
        

tokens = encoding.tokens()
token = tokens.pop(0)
letter = token[0].lower()
expected_key = keys[letter]
print(token, letter, expected_key)
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    if event.type == pygame.KEYDOWN:
      pressed = pygame.key.get_pressed()
      if pressed[expected_key]:
        token = tokens.pop(0)
        letter = token[0].lower()
        expected_key = keys[letter]
        print(token, letter, expected_key)

    screen.refresh()

