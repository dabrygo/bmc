'''Collection of data specific to a single game.'''

import csv
import os.path
import time

import Score

class Game:
  def __init__(self, mode_code, n_guesses=0):
    self._correct = Score.Correct()
    self._incorrect = Score.Incorrect()
    self._hints = Score.Hints()
    self._timer = Score.Timer()
    self._total = Score.Total.Standard(
      correct=self._correct,
      incorrect=self._incorrect,
      hints=self._hints,
      timer=self._timer,
    )
    self._start_time = time.strftime("%Y-%m-%d %H:%M:%S")
    self._mode_code = mode_code
    if mode_code == 1:
      assert n_guesses > 0
      self._guesses = Score.Guesses(count_start=n_guesses)
    else:
      self._guesses = None

  def clock_ticked(self):
    self._timer.increment()

  def time(self):
    return self._timer.value()

  def timer(self):
    return self._timer

  def guess_right(self):
    self._correct.increment()
    if self._guesses:
      self._guesses.reset()

  def correct(self):
    return self._correct

  def n_correct(self):
    return self._correct.value()

  def request_hint(self):
    self._hints.increment()

  def hints(self):
    return self._hints

  def n_hints(self):
    return self._hints.value()

  def guess_wrong(self):
    self._incorrect.increment()
    if self._guesses:
      self._guesses.decrement()

  def incorrect(self):
    return self._incorrect

  def n_incorrect(self):
    return self._incorrect.value()

  def score(self):
    return self._total.value()

  def total(self):
    return self._total

  def guesses(self):
    return self._guesses

  def n_guesses(self):
    if self._guesses:
      return self._guesses.value()
    else:
      return None

  def save_to_file(self):
    game_data = {
      'Time_Start': self._start_time,
      'Score': self.score(),
      'Correct': self.n_correct(), 
      'Incorrect': self.n_incorrect(), 
      'Hints': self.n_hints(), 
      'Time': self.time(),
      'Game_Mode': self._mode_code,
    }
    out_file = 'rsc/scores.csv'
    if not os.path.exists(out_file):
      write_header = True
    else:
      write_header = False
    with open(out_file, 'a', newline='') as csvfile:
      fieldnames = game_data.keys()
      writer = csv.DictWriter(
        csvfile, delimiter=',', fieldnames=fieldnames,
      )
      if write_header:
        writer.writeheader()
      writer.writerow(game_data) 


