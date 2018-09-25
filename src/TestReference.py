import Reference
import unittest

class TestStandard(unittest.TestCase):
  def test_book(self):
    reference = Reference.Standard('John 11:35')
    self.assertEqual('John', reference.book())

  def test_numbered_book(self):
    reference = Reference.Standard('1 John 1:1')
    self.assertEqual('1 John', reference.book())

  def test_roman_numerals(self):
    reference = Reference.Standard('III John 1:1')
    self.assertEqual('III John', reference.book())

  def test_multiword_book(self):
    reference = Reference.Standard('Song of Solomon 1:1')
    self.assertEqual('Song of Solomon', reference.book())

  def test_chapter(self):
    reference = Reference.Standard('John 11:35')
    self.assertEqual(11, reference.chapter())

  def test_verse(self):
    reference = Reference.Standard('John 11:35')
    self.assertEqual(35, reference.verse())


if __name__ == '__main__':
  unittest.main()
