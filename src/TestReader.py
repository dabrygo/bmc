import unittest

import Parser
import Verse


class TestSimple(unittest.TestCase):
  def test_parse(self):
    lines = ['Section', 'Book 1:23 Verse verse verse']
    parser = Parser.Simple(lines)
    expected = Verse.Fake(section='Section', reference='Book 1:23', text='Verse verse verse')
    verses = parser.parse(max_width=100)
    actual = verses[0]
    self.assertEqual(expected, actual)


if __name__ == '__main__':
  unittest.main()
