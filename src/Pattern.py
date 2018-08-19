import re

class Pattern:
  def __init__(self, regex, line):
    self._regex = regex
    self._line = line

  def _match(self):
    return re.search(self._regex, self._line) 

  def matches(self):
    return self._match() is not None 

  def group(self, index):
    match = self._match()
    if match is None:
      raise Exception(f"Regex '{self._regex}' does not match '{self._line}'")
    return match.group(index)


class Verse(Pattern):
  def __init__(self, line):
    super().__init__(r'(\w+ \d+:\d+) (.+)', line)


