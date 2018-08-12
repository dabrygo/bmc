import unittest

import Encoding


class TestBlank(unittest.TestCase):
  def test_token(self):
    encoding = Encoding.Blank.hangman('The rain in Spain')
    self.assertEqual(['The', 'rain', 'in', 'Spain'], encoding.tokens())

  def test_encoded(self):
    plaintext = 'Paul, a prisoner of Christ Jesus, and Timothy our brother'
    encoding = Encoding.Blank.hangman(plaintext)
    expected = '____, _ ________ __ ______ _____, ___ _______ ___ _______'
    self.assertEqual(expected, encoding.encoded())


if __name__ == '__main__':
  unittest.main()


