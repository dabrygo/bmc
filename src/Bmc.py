'''
Entry point file for game.
'''

import csv
import os.path
import sys
import textwrap
import time

import pygame
import pygame_gui

import Color
import Display
import Parser
import Reader
import Score
import Sample
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

manager = pygame_gui.UIManager(
    (width, height), 
    theme_path="rsc/bmc_default_theme.json",
)

# Game timer
clock = pygame.time.Clock()
TIMER_EVENT = pygame.USEREVENT + 1 # Define a unique custom event ID
# Set the timer to trigger every second 
MS_PER_SECOND = 1000
pygame.time.set_timer(TIMER_EVENT, millis=MS_PER_SECOND) 

max_chars = 60
wrapper = textwrap.TextWrapper(max_chars)

correct = Score.Correct()
correct_box = Display.ScoreBox(manager, "Correct", (0 * Display.ScoreBox.BOX_SIZE, 0))

incorrect = Score.Incorrect()
incorrect_box = Display.ScoreBox(manager, "Incorrect", (1 * Display.ScoreBox.BOX_SIZE, 0))

hints = Score.Hints()
hints_box = Display.ScoreBox(manager, "Hints", (2 * Display.ScoreBox.BOX_SIZE, 0))

timer = Score.Timer()
timer_box = Display.ScoreBox(manager, "Timer", (3 * Display.ScoreBox.BOX_SIZE, 0))

total = Score.Total.Standard(correct, incorrect, hints, timer)
total_box = Display.ScoreBox(manager, "Score", (4 * Display.ScoreBox.BOX_SIZE, 0))


def redraw(lines, screen):
  displays = []
  for i, line in enumerate(lines):
    x = 0 
    y = Display.ScoreBox.BOX_SIZE + i * font_size
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

start_time = time.strftime("%Y-%m-%d %H:%M:%S")

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
    time_delta = clock.tick(60) / MS_PER_SECOND
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      # Timer
      if event.type == TIMER_EVENT:
        redraw(lines, screen)
        timer.increment()
        timer_box.set_tally(timer.count())
        total_box.set_tally(total.value())

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
          correct_box.set_tally(correct.count())
          redraw(lines, screen)
        elif pressed_keys[HINT_KEY]:
          sample.hint()
          revealed = sample.text()
          lines = wrapper.wrap(revealed)
          section = verse.section()
          lines.insert(0, section)
          reference = verse.reference()
          lines.insert(1, reference)
          redraw(lines, screen)          
          hints.increment()
          hints_box.set_tally(hints.count())
        else:
          incorrect.increment()
          incorrect_box.set_tally(incorrect.count())
          redraw(lines, screen)
    
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen.surface())

    pygame.display.update()

  time.sleep(delay)

# Score screen
user_exit = False
y = Display.ScoreBox.BOX_SIZE
y_pad = 10
continue_y = y + y_pad
continue_textbox = Display.TextBox.default_modified('Press any key to exit', font, text_color, 0, continue_y)
displays = [continue_textbox]
screen.blit(displays)
while not user_exit:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      user_exit = True

game_data = {
  'Time_Start': start_time,
  'Score': total.value(),
  'Correct': correct.count(), 
  'Incorrect': correct.count(), 
  'Hints': hints.count(), 
  'Time': timer.count(),
}
out_file = 'rsc/scores.csv'
if not os.path.exists(out_file):
  write_header = True
else:
  write_header = False
with open(out_file, 'a', newline='') as csvfile:
  writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=game_data.keys())
  if write_header:
    writer.writeheader()
  writer.writerow(game_data)