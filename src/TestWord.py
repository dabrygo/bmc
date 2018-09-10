import unittest

import Word

class TestClassic(unittest.TestCase):
  def test_status(self):
    word = Word.Classic('bird', '*')
    self.assertEqual('****', word.hide())

  def test_hint(self):
    word = Word.Classic('at', '*')
    self.assertEqual('*t', word.hint())
    self.assertEqual('at', word.hint())
    try:
      word.hint()
      self.fail()
    except Exception:
      pass

  def test_guess(self):
    word = Word.Classic('bird', '*')
    self.assertEqual('****', word.guess('a'))
    self.assertEqual('****', word.guess('1'))
    self.assertEqual('****', word.guess(','))
    self.assertEqual('bird', word.guess('B'))


if __name__ == '__main__':
  unittest.main()
