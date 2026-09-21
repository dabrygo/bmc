import unittest

import Score

class TestScore(unittest.TestCase):
  def assertIsPositive(self, n):
    self.assertTrue(n > 0)

  def assertIsNegative(self, n):
    self.assertTrue(n < 0)

  def assertIsZero(self, n):
    self.assertEqual(0, n)

  def test_init(self):
    score = Score.Total.Fake(
      n_correct=0, n_incorrect=0, n_hints=0, time=0
    )
    self.assertIsZero(score.value())

  def test_correct(self):
    score = Score.Total.Fake(n_correct=1)
    self.assertIsPositive(score.value())

  def test_incorrect(self):
    score = Score.Total.Fake(n_incorrect=1)
    self.assertIsNegative(score.value())

  def test_hint(self):
    score = Score.Total.Fake(n_hints=1)
    self.assertIsNegative(score.value())

  def test_time(self):
    score = Score.Total.Fake(time=1)
    self.assertIsNegative(score.value())


if __name__ == '__main__':
  unittest.main()
