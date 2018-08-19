import Pattern
import Verse

class Reader:
  def __init__(self, filename):
    self._filename = filename

  def read(self, max_width):
    verses = []
    section = ""
    with open(self._filename) as f:
      for line in f:
        pattern = Pattern.Verse(line)
        if not pattern.matches():
          section = line
        else:
          verse = Verse.Default(section, line, max_width) 
          verses.append(verse)
    return verses


if __name__ == '__main__':
  reader = Reader('Philemon.txt')
  verses = reader.read(max_width=60)
  for verse in verses:
    print(f'{verse.section()} ({verse.reference()}) "{verse.text()}"')


