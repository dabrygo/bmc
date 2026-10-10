import unittest

from bmc import Minigame
from bmc import Verse

class TestMinigame(unittest.TestCase):
  def test_content(self):
    verse = Verse.Fake(
      section='Section',
      reference='Book 1:23',
      text='Verse verse verse',
    )
    minigame = Minigame.Minigame(verse=verse)
    self.assertEqual(verse.text(), minigame.content())