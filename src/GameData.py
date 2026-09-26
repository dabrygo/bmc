'''Collection of data specific to a single game.'''

import csv
import os.path
import time

import Score

class Session:
  def __init__(self, mode_code, max_attempts=0):
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
    self._attempts = Score.Attempts(count_start=0, count_max=max_attempts)

  def clock_ticked(self):
    self._timer.increment()

  def time(self):
    return self._timer.value()

  def timer(self):
    return self._timer

  def guess_right(self):
    self._correct.increment()
    self._attempts.reset()

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
    self._attempts.increment()

  def incorrect(self):
    return self._incorrect

  def n_incorrect(self):
    return self._incorrect.value()

  def score(self):
    return self._total.value()

  def total(self):
    return self._total

  def attempts(self):
    return self._attempts

  def n_attempts(self):
    return self._attempts.value()

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


