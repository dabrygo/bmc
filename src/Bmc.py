'''
Entry point file for game.
'''

import os.path
import sys
import textwrap
import time

import pygame

import Color
import Display
import Parser
import Reader
import Sample
import Score
import Tokens

# Changeable Properties
background = Color.Black()
text_color = Color.White()
font_size = 12
font = pygame.font.SysFont('consolas', size=font_size)
delay = 0.25  # seconds to wait before changing a screen

# Derived Properties
n_cols = 120
n_rows = 30
avg_char_height = ((.7 + 1.0) / 2) * font_size
avg_char_width = .6 * font_size
width = n_cols * avg_char_width
height = n_rows * avg_char_height
screen = Display.Screen.size_and_color(width=width, height=height, color=background)

# Game timer
clock = pygame.time.Clock()
TIMER_EVENT = pygame.USEREVENT + 1 # Define a unique custom event ID
# Set the timer to trigger every second 
MS_PER_SECOND = 1000
pygame.time.set_timer(TIMER_EVENT, millis=MS_PER_SECOND) 

max_chars = 60
wrapper = textwrap.TextWrapper(max_chars)

correct = Score.Correct()
incorrect = Score.Incorrect()
hints = Score.Hints()
timer = Score.Timer()
total = Score.Total.Standard(correct, incorrect, hints, timer)


def next_start_x(textbox, *, x_offset):
  '''Where horizontally to start the next textbox'''
  x_pad = avg_char_width * 5
  surface = textbox.surface()
  rect = surface.get_rect()
  x_rect_start = x_offset + rect.x
  rect_width = rect.width
  x_rect_end = x_rect_start + rect_width 
  return x_rect_end + x_pad

def redraw_tallies(screen):
  global correct 
  global incorrect
  global hints
  global timer
  global total

  correct_text = f'Correct: {correct.count():05d}'
  correct_start = 0
  correct_textbox = Display.TextBox.default_modified(correct_text, font, text_color, correct_start, 0)

  incorrect_text = f'Incorrect: {incorrect.count():05d}'
  incorrect_start = next_start_x(correct_textbox, x_offset=0)
  incorrect_textbox = Display.TextBox.default_modified(incorrect_text, font, text_color, incorrect_start, 0)

  hint_text = f'Hints: {hints.count():05d}'
  hint_start = next_start_x(incorrect_textbox, x_offset=incorrect_start)
  hint_textbox = Display.TextBox.default_modified(hint_text, font, text_color, hint_start, 0)

  timer_text = f'Timer: {timer.count():05d}'
  timer_start = next_start_x(hint_textbox, x_offset=hint_start)
  timer_textbox = Display.TextBox.default_modified(timer_text, font, text_color, timer_start, 0)

  score_text = f'Score: {total.value():07d}'
  score_start = next_start_x(timer_textbox, x_offset=timer_start)
  score_textbox = Display.TextBox.default_modified(score_text, font, text_color, score_start, 0)

  displays = []
  displays.append(correct_textbox)
  displays.append(incorrect_textbox)
  displays.append(hint_textbox)
  displays.append(timer_textbox)
  displays.append(score_textbox)

  screen.blit(displays)

  return displays


def redraw(lines, screen):
  displays = redraw_tallies(screen)
  for i, line in enumerate(lines):
    x = 0
    y = i * font_size
    textbox = Display.TextBox.default_modified(line, font, text_color, x, y)

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

directory = 'rsc/books'
#book = 'John'
book = '3_John'
#book = 'Philemon' 
filename = book + '.txt'
path = os.path.join(directory, filename)
reader = Reader.File(path)
lines = reader.lines()
parser = Parser.Simple(lines)
verses = parser.parse(max_width=max_chars)

for verse in verses:
  text = verse.text()
  tokens = Tokens.Classic(text)
  tokenized = tokens.tokenize()
  sample = Sample.Classic(tokenized)
  lines = wrapper.wrap(sample.text())
  section = verse.section()
  lines.insert(0, section)
  reference = verse.reference()
  lines.insert(1, reference)
  redraw(lines, screen)

  while sample.guessable():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      # Timer
      if event.type == TIMER_EVENT:
        timer.increment()
        redraw(lines, screen)

      if event.type == pygame.KEYDOWN:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[sample.key()]:
          sample.guess(letters[sample.key()])
          revealed = sample.text()
          lines = wrapper.wrap(revealed)
          section = verse.section()
          lines.insert(0, section)
          reference = verse.reference()
          lines.insert(1, reference)
          correct.increment()
          redraw(lines, screen)          
        elif pressed_keys[HINT_KEY]:
          sample.hint()
          revealed = sample.text()
          lines = wrapper.wrap(revealed)
          section = verse.section()
          lines.insert(0, section)
          reference = verse.reference()
          lines.insert(1, reference)
          hints.increment()
          redraw(lines, screen)          
        else:
          incorrect.increment()
          redraw(lines, screen)          

  time.sleep(delay)
 
