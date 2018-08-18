import pygame
import sys
import textwrap
import time

import Color
import Display
import Decoding
import Encoding

# Changeable Properties
background = Color.Black()
text_color = Color.White()
font_size = 32
font = pygame.font.SysFont('courier', font_size, bold=True)
delay = 0.25  # seconds to wait before changing a screen

# Derived Properties
width = 1200
height = 400
screen = Display.Screen.size_and_color(width=width, height=height, color=background)

max_chars = 60
wrapper = textwrap.TextWrapper(max_chars)

def redraw(lines, screen):
  displays = []
  for i, line in enumerate(lines):
    x = 0
    y = i * font_size
    textbox = Display.TextBox.default(line, text_color, x, y)
    displays.append(textbox)
  screen.blit(displays)


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

verse_1 = 'Paul, a prisoner of Christ Jesus, and Timothy, our brother, To Philemon our dear friend and fellow worker,'
verse_2 = 'to Apphia our sister, to Archippus our fellow soldier and to the church that meets in your home:'
verse_3 = 'Grace to you and peace from God our Father and the Lord Jesus Christ.'

verses = [verse_1, verse_2, verse_3]

for verse in verses:
  encoding = Encoding.Blank.hangman(verse)
  encoded = encoding.encoded()
  starts = encoding.starts()
  lines = wrapper.wrap(encoded)
  redraw(lines, screen)

  tokens = encoding.tokens()
  token = tokens.pop(0)
  start = starts.pop(0)
  letter = token[0].lower()
  expected_key = keys[letter]
  decoding = Decoding.Decoding(verse, encoding)

  this_verse = True
  while this_verse:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      if event.type == pygame.KEYDOWN:
        pressed = pygame.key.get_pressed()
        if pressed[expected_key]:
          revealed = decoding.reveal()
          lines = wrapper.wrap(revealed)
          print(lines)
          redraw(lines, screen)          
          if not tokens:
            this_verse = False
            time.sleep(delay)
          else:
            token = tokens.pop(0)
            letter = token[0].lower()
            start = starts.pop(0)
            expected_key = keys[letter]

