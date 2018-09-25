import pygame
import os.path
import sys
import textwrap
import time

import Color
import Display
import Parser
import Reader
import Reference
import Sample
import Tokens
import Word

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

letters = {
         pygame.K_a: 'a',
         pygame.K_b: 'b',
         pygame.K_c: 'c',
         pygame.K_d: 'd',
         pygame.K_e: 'e',
         pygame.K_f: 'f',
         pygame.K_g: 'g',
         pygame.K_h: 'h',
         pygame.K_i: 'i',
         pygame.K_j: 'j',
         pygame.K_k: 'k',
         pygame.K_l: 'l',
         pygame.K_m: 'm',
         pygame.K_n: 'n',
         pygame.K_o: 'o',
         pygame.K_p: 'p',
         pygame.K_q: 'q',
         pygame.K_r: 'r',
         pygame.K_s: 's',
         pygame.K_t: 't',
         pygame.K_u: 'u',
         pygame.K_v: 'v',
         pygame.K_w: 'w',
         pygame.K_x: 'x',
         pygame.K_y: 'y',
         pygame.K_z: 'z',
       }

HINT_KEY = pygame.K_SLASH

args = sys.argv
if len(args) > 1:
  book = sys.argv[1]
else:
  book = 'John'

if len(args) > 2:
  start = sys.argv[2]
else:
  start = '1:1'

if len(args) > 3:
  end = sys.argv[3]
else:
  end = None

filename = book + '.txt'
path = os.path.join('books', filename)
reader = Reader.File(path)
lines = reader.lines()
parser = Parser.Simple(lines)
verses = parser.parse(max_width=max_chars)

parts = start.split(':')
start_chapter = int(parts[0])
start_verse = int(parts[1])
#start_reference = Reference.Fields(book, start_chapter, start_verse)

after_start = []
for verse in verses:
  reference = verse.reference()
  if reference.chapter() < start_chapter:
    continue
  if reference.verse() < start_verse:
    continue
  after_start.append(verse)
to_use = after_start

if end:
  parts = end.split(':')
  end_chapter = int(parts[0])
  end_verse = int(parts[1])

  before_end = []
  for verse in after_start:
    reference = verse.reference()
    if reference.chapter() == start_chapter and reference.verse() == end_verse:
      break
    before_end.append(verse)
  before_end.append(verse)
  to_use = before_end

for verse in to_use:
  text = verse.text()
  tokens = Tokens.Classic(text)
  tokenized = tokens.tokenize()
  sample = Sample.Classic(tokenized)
  lines = wrapper.wrap(sample.text())
  section = verse.section()
  lines.insert(0, section)
  reference = str(verse.reference())
  lines.insert(1, reference)
  redraw(lines, screen)

  while sample.guessable():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      if event.type == pygame.KEYDOWN:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[sample.key()]:
          sample.guess(letters[sample.key()])
          revealed = sample.text()
          lines = wrapper.wrap(revealed)
          section = verse.section()
          lines.insert(0, section)
          reference = str(verse.reference())
          lines.insert(1, reference)
          redraw(lines, screen)          
        if pressed_keys[HINT_KEY]:
          sample.hint()
          revealed = sample.text()
          lines = wrapper.wrap(revealed)
          section = verse.section()
          lines.insert(0, section)
          reference = str(verse.reference())
          lines.insert(1, reference)
          redraw(lines, screen)          
  time.sleep(delay)
 
