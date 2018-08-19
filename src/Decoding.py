import Encoding

class Decoding:
  def __init__(self, text, encoding):
    self._text = text
    self._encoding = encoding
    self._index = 0

  def reveal(self):
    indices = self._encoding.starts()
    index = indices[self._index]
    tokens = self._encoding.tokens()
    token = tokens[self._index]
    word = index + len(token)
    shown = self._text[:word]
    encoded = self._encoding.encoded()
    hidden = encoded[word:]
    self._index += 1 
    return shown + hidden



