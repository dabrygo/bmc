import unittest

import Decoding
import Encoding

class TestDecoding(unittest.TestCase):
  def test(self):
    text = "Paul, a prisoner,"
    encoding = Encoding.Blank.hangman(text)
    self.assertEqual("____, _ ________,", encoding.encoded())
    decoding = Decoding.Decoding(text, encoding)
    revealed = decoding.reveal()
    self.assertEqual("Paul, _ ________,", revealed)

