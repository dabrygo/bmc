'''Keeps track of how well the user plays a game.'''


class Tally:
  '''Keeps track of how many times something happens.'''

  def __init__(self):
    self._count = 0

  def increment(self):
    self._count += 1

  def count(self):
    return self._count


class Correct(Tally):
  '''Keeps track of how many times user enters correct inputs.'''

  def __init__(self):
    super().__init__()


class Incorrect(Tally):
  '''Keeps track of how many times user enters incorrect inputs.'''

  def __init__(self):
    super().__init__()


class Hints(Tally):
  '''Keeps track of how many times user requests hints.'''

  def __init__(self):
    super().__init__()


class Timer(Tally):
  '''Keeps track of how many seconds have passed.'''

  def __init__(self):
    super().__init__()


class Score:
  '''Calculates the score of a tally.'''

  def __init__(self, tally, *, multiplier=1):
    self._tally = tally
    self._multiplier = multiplier

  def value(self):
    return self._tally.count() * self._multiplier


class Total:
  '''Calculates the total score.'''

  @classmethod
  def Standard(cls, correct, incorrect, hints, timer):
    correct_score = Score(correct, multiplier=100)
    incorrect_score = Score(incorrect, multiplier=50)
    hints_score = Score(hints, multiplier=25)
    timer_score = Score(timer, multiplier=5)
    return cls(correct_score, incorrect_score, hints_score, timer_score)

  def __init__(self, correct, incorrect, hints, timer):
    self._correct = correct
    self._incorrect = incorrect
    self._hints = hints
    self._timer = timer

  def value(self):
    correct = self._correct.value()
    incorrect = self._incorrect.value()
    hints  = self._hints.value()
    timer = self._timer.value()
    return correct - incorrect - hints - timer