import unittest

from src.bmc import Material 
from src.bmc import Verse


class TestBook(unittest.TestCase):
  def test_parse(self):
    lines = ['Book 1:23 Verse verse verse']
    parser = Material.Book(lines)
    expected = Verse.Fake(
      section='',
      reference='Book 1:23',
      text='Verse verse verse'
    )
    verses = parser.parse()
    actual = verses[0]
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
