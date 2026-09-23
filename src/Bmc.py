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
import GameMode
import Parser
import Reader
import Score

# Changeable Properties
background = Color.Black()
text_color = Color.White()
font_size = 24
font_face = 'Consolas'
font_path = "c:/windows/fonts/consolas.ttf"
font = pygame.font.SysFont(font_face, size=font_size)
delay = 0.25  # seconds to wait before changing a screen

# Derived Properties
#n_cols = 120
#n_rows = 30
#avg_char_height = ((.7 + 1.0) / 2) * font_size
#avg_char_width = .6 * font_size
#width = n_cols * avg_char_width
#height = n_rows * avg_char_height
width = 800
height = 400
screen = Display.Screen.size_and_color(width=width, height=height, color=background)

manager = pygame_gui.UIManager(
    (width, height), 
    theme_path="rsc/bmc_default_theme.json",
)

manager.add_font_paths(font_face, font_path)
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

total = Score.Total.Standard(
  correct=correct, incorrect=incorrect, hints=hints, timer=timer
)
total_box = Display.ScoreBox(manager, "Score", (4 * Display.ScoreBox.BOX_SIZE, 0))

screen_lines = []
N_SCREEN_LINES = 8

def init_screen():
  global screen_lines

  screen_lines = []
  box_height = font_size + 10
  for i in range(N_SCREEN_LINES):
    x = 0 
    y = Display.ScoreBox.BOX_SIZE + i * box_height 
    text_box = Display.ContentBox(
      manager=manager, 
      label=f"verse_{i}",
      position=(x, y), 
      size=(600, box_height), 
      text=""
    )
    screen_lines.append(text_box)

def update_screen_text(raw_text, verse=None):
  global screen_lines

  # Wrap text to fit on screen
  wrapped = wrapper.wrap(raw_text)
  if verse:
    section = verse.section()
    wrapped.insert(0, section)
    reference = verse.reference()
    wrapped.insert(1, reference)
  assert len(wrapped) <= N_SCREEN_LINES

  for i in range(N_SCREEN_LINES):
    text_box = screen_lines[i]
    if i < len(wrapped):
      line = wrapped[i]
    else:
      line = ""
    text_box.set_text(line)

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
verses = parser.parse()

start_time = time.strftime("%Y-%m-%d %H:%M:%S")

init_screen()
for verse in verses:
  mode = GameMode.AllBlank(verse)

  content = mode.content()
  update_screen_text(raw_text=content, verse=verse)
   
  while mode.must_guess_again():
    time_delta = clock.tick(60) / MS_PER_SECOND
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      # Timer
      if event.type == TIMER_EVENT:
        timer.increment()
        time_now = timer.count()
        timer_box.set_tally(time_now)
        updated_score = total.value()
        total_box.set_tally(updated_score)

      if event.type == pygame.KEYDOWN:
        pressed_keys = pygame.key.get_pressed()

        expected_input = mode.expected_input()
        is_correct = pressed_keys[expected_input]

        is_hint = pressed_keys[HINT_KEY]

        if is_correct:
          correct.increment()
          n_correct = correct.count()
          correct_box.set_tally(n_correct)

          text = mode.on_correct_guess()
          update_screen_text(text, verse=verse)
        elif is_hint:
          hints.increment()
          n_hints = hints.count()
          hints_box.set_tally(n_hints)

          text = mode.on_hint()
          update_screen_text(text, verse=verse)
        else: # is_incorrect
          incorrect.increment()
          n_incorrect = incorrect.count()
          incorrect_box.set_tally(n_incorrect)

          text = mode.on_incorrect_guess()
          update_screen_text(text, verse=verse)

        manager.process_events(event)

    manager.update(time_delta)
    background = screen.surface()
    manager.draw_ui(background)

    pygame.display.update()

  time.sleep(delay)

# Score screen
user_exit = False
text = 'Press any key to exit'
update_screen_text(text)

manager.update(time_delta)
background = screen.surface()
manager.draw_ui(background)

pygame.display.update()

while not user_exit:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    if event.type == pygame.KEYDOWN:
        user_exit = True

# Save game data to file
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