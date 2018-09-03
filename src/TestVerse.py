import unittest

import Verse

class TestDefault(unittest.TestCase):
  def test_equals(self):
    a = Verse.Default(section='Section', text='Book 1:23 Verse verse verse')
    b = Verse.Default(section='Section', text='Book 1:23 Verse verse verse')
    self.assertEqual(a, a)
    self.assertEqual(a, b)
    self.assertEqual(b, a)


  def test_reference(self):
    verse = Verse.Default(section='Section', text='Book 1:23 Verse verse verse')
    self.assertEqual('Book 1:23', verse.reference())

  def test_section(self):
    verse = Verse.Default(section='Section', text='Book 1:23 Verse verse verse')
    self.assertEqual('Section', verse.section())

  def test_text(self):
    verse = Verse.Default(section='Section', text='Book 1:23 Verse verse verse')
    self.assertEqual('Verse verse verse', verse.text())

  def test_lines(self):
    verse = Verse.Default(section='Section', text='Book 1:23 Verse verse verse', max_width=None)
    self.assertEqual('Verse verse verse', verse.lines())

    verse = Verse.Default(section='Section', text='Book 1:23 Verse verse verse', max_width=8)
    self.assertEqual(['Verse', 'verse', 'verse'], verse.lines())


class TestFake(unittest.TestCase):
  def test_equals(self):
    verse = Verse.Default(section='Section', text='Book 1:23 Verse verse verse')
    fake = Verse.Fake(section='Section', reference='Book 1:23', text='Verse verse verse')
    self.assertEqual(verse, fake)
    self.assertEqual(fake, verse)

  def test_reference(self):
    verse = Verse.Fake(section='Section', reference='Book 1:23', text='Verse verse verse')
    self.assertEqual('Book 1:23', verse.reference())

  def test_section(self):
    verse = Verse.Fake(section='Section', reference='Book 1:23', text='Verse verse verse')
    self.assertEqual('Section', verse.section())

  def test_text(self):
    verse = Verse.Fake(section='Section', reference='Book 1:23', text='Verse verse verse')
    self.assertEqual('Verse verse verse', verse.text())

  @unittest.expectedFailure
  def test_lines(self):
    verse = Verse.Fake(section='Section', reference='Book 1:23', text='Verse verse verse')
    verse.lines()  


if __name__ == '__main__':
  unittest.main()
