import unittest


class TestClassic(unittest.TestCase):
  @unittest.skip("TBD")
  def test_words(self):
    self.fail()


if __name__ == '__main__':
  unittest.main()

