import unittest

import Tokens
import Word

class TestTokens(unittest.TestCase):
  def test_text(self):
    tokens = Tokens.Classic('I say, "Hi!"')
    self.assertEqual('_ ___, "__!"', tokens.text()) 
    tokens.shift()
    self.assertEqual('I ___, "__!"', tokens.text())
    tokens.shift()
    self.assertEqual('I say, "__!"', tokens.text())
    tokens.shift()
    self.assertEqual('I say, "Hi!"', tokens.text())
    try:
      tokens.shift()
      self.fail()
    except Exception:
      pass

  def test_current(self):
    tokens = Tokens.Classic('I say, "Hi!"')
    self.assertEqual('I', tokens.current().show()) 

  def test_shift(self):
    tokens = Tokens.Classic('I say, "Hi!"')
    self.assertEqual("I", tokens.current().show())
    tokens.shift()
    self.assertEqual("say", tokens.current().show())
    tokens.shift()
    self.assertEqual("Hi", tokens.current().show())
    try:
      tokens.shift()
      self.fail()
    except Exception:
      pass


if __name__ == '__main__':
  unittest.main()
