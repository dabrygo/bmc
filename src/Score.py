'''Keeps track of how well the user plays a game.'''


class Tally:
  def __init__(self):
    self._count = 0

  def increment(self):
    self._count += 1

  def count(self):
    return self._count


class Correct(Tally):
  def __init__(self):
    super().__init__()


class Incorrect(Tally):
  def __init__(self):
    super().__init__()


class Hints(Tally):
  def __init__(self):
    super().__init__()