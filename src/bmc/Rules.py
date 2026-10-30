import abc
import csv
import os
import random
import shutil
import sys

import pygame

from bmc import GameView


class Sequence(abc.ABC):
  @abc.abstractmethod
  def verses(self):
    pass


class Custom(Sequence):
  def __init__(self, sequence_file):
    self._sequence_file = sequence_file

  def verses(self):
    return self._sequence_file.verses()


class Sequential(Sequence):
  def __init__(self, material):
    self._material = material

  def verses(self):
    return sorted(self._material)


class Reverse(Sequence):
  def __init__(self, material):
    self._material = material

  def verses(self):
    return sorted(self._material, reverse=True)


class Random(Sequence):
  def __init__(self, material):
    self._material = material

  def verses(self):
    material = self._material.copy()
    k = len(material)
    return random.sample(material, k)


def kp_step(n, chunk_size=5):
    if n % chunk_size == 1:
        return [n]

    # New Verse
    x = [n] 

    # Together
    n_chunks = (n-1) // chunk_size
    start = (chunk_size * n_chunks) + 1
    together = tuple(i for i in range(start, n+1))
    x.append(together)

    # Forwards and backwards
    forwards = tuple(i for i in range(start, n+1))
    backwards = tuple(i for i in range(n, start - 1, -1))
    fwd_and_bkwd = tuple([forwards, backwards])
    x.append(fwd_and_bkwd)

    if n > chunk_size and n % chunk_size == 0:
        all_in_order = tuple(i for i in range(1, n+1))
        x.append(all_in_order)

    return x


def kp(n, chunk_size=5):
    x = []
    for i in range(1, n+1):
        step = kp_step(i, chunk_size=chunk_size)
        new = []
        together = []
        forwards = []
        backwards = []
        all_in_order = []
        if len(step) == 1:
            new = step[0]
        elif len(step) == 3:
            new, together, fwd_and_bkwd = step
            forwards, backwards = fwd_and_bkwd
        elif len(step) == 4:
            new, together, fwd_and_bkwd, all_in_order = step
            forwards, backwards = fwd_and_bkwd
        else:
            raise ValueError
        x.append(new)
        x.extend(together)
        x.extend(forwards)
        x.extend(backwards)
        x.extend(all_in_order)
    if n % chunk_size != 0:
        # Make sure to end with all verses in order
        x.extend([i for i in range(1, n+1)])
    return x


class MemorizeKP(Sequence):
  def __init__(self, material):
    self._material = material

  def verses(self):
    n = len(self._material)
    return [self._material[idx-1] for idx in kp(n)]


class SequenceFile:
  def __init__(self, filename, material):
    self._filename = filename
    self._material = material

  @classmethod
  def from_file(cls, material):
    return cls('rsc/sequence.csv', material)

  def _read(self):
    message = f"Custom sequence file not found: {self._filename}"
    if not os.path.exists(self._filename):
      raise FileNotFoundError(message)
    with open(self._filename, newline='') as csvfile:
      lines = []
      reader = csv.reader(csvfile)
      for i, row in enumerate(reader):
        is_header_row = i == 0
        if is_header_row:
          continue
        lines.append(row)
    return lines

  def update_file(self, new_sequence):
    with open(self._filename, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['n_verses', 'type', 'verse'])
      for verse in new_sequence:
        row = [1, 'reference', verse.reference()]
        writer.writerow(row)

  def archive_file(self, start_time):
    if not os.path.exists(self._filename):
      raise FileNotFoundError(f"Custom sequence file not found: {self._filename}")

    archive_dir = 'rsc/sequences'
    if not os.path.exists(archive_dir):
      os.makedirs(archive_dir)

    original = self._filename
    basename = os.path.basename(original)
    filename, _ = os.path.splitext(basename)
    suffix = start_time.replace(':', '-').replace(' ', 'T')
    archive = f'rsc/sequences/{filename}_{suffix}.csv'
    shutil.copy(original, archive)

  def verses(self):
    sequence = []
    lines = self._read()
    for i, row in enumerate(lines):
      n_verses = self._n_verses(row, i)
      type_ = self._type(row, i)
      verses = self._verses(row, i)
      verse, *_ = verses
      material_verse = self._find_verse_in_material(verse)
      sequence.append(material_verse)
    return sequence

  def _n_verses(self, row, i):
    n_verses = int(row[0])
    if n_verses < 0:
      raise ValueError(f"Expected at least one verse but found {n_verses} in line {i}")
    if n_verses > 1:
      raise NotImplementedError(f"More than one verse ({n_verses} in line {i}) not yet supported")
    return n_verses

  def _type(self, row, i):
    type_ = row[1]
    if type_ == 'consecutive':
      raise NotImplementedError(f"'consecutive' not yet supported (line {i})")
    elif type_ == 'reference':
      return type_
    else:
      raise ValueError(f"Unknown type '{type_}' in line {i}")

  def _verses(self, row, i):
    verses = row[2:]
    if len(verses) == 0:
      raise ValueError(f"Expected at least one verse but found none in line {i}")
    if len(verses) > 1:
      raise NotImplementedError(f"More than one verse ({len(verses)} in line {i}) not yet supported")
    return verses

  def _find_verse_in_material(self, verse):
    for material_verse in self._material:
      if material_verse.reference() == verse:
        return material_verse
    raise ValueError(f"Could not find verse {verse}")


class Rules:
  def __init__(self, sequence, seed=None):
    self._sequence = sequence
    if seed is not None:
      random.seed(seed)

  @classmethod
  def from_config(cls, config):
    return cls(config.sequence())

  def sequenced(self, material, start_time):
    '''Choose order to present material to user'''
    sequence = self.sequence()
    sequence_file = SequenceFile.from_file(material)
    if sequence == 'custom':
      reordered_material = Custom(sequence_file)
    elif sequence == 'sequential':
      reordered_material = Sequential(material)
    elif sequence == 'reverse':
      reordered_material = Reverse(material)
    elif sequence == 'random':
      reordered_material = Random(material)
    elif sequence == 'memorize_kp':
      reordered_material = MemorizeKP(material)
    else:
      assert False, f"Unknown sequence code: {sequence}"
    # Update is redundant if custom
    screens = reordered_material.verses()
    sequence_file.update_file(screens)
    sequence_file.archive_file(start_time)
    return screens
     
  def sequence(self):
    '''Choose order to present material to user'''
    supported_sequences = ['custom', 'sequential', 'reverse', 'random', 'memorize_kp']
    if self._sequence in supported_sequences:
      return self._sequence
    else:
      raise ValueError(f"Unknown sequence code: {self._sequence}")

  def choose_minigame(self):
    '''Allow the user to choose a minigame.'''
    selection_view = GameView.SelectMinigame()
    while True:
      selection_view.refresh_screen()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYDOWN:
          pressed_keys = pygame.key.get_pressed()

          if pressed_keys[pygame.K_1]:
            return 1
          elif pressed_keys[pygame.K_2]:
            return 2
          elif pressed_keys[pygame.K_3]:
            return 3
          elif pressed_keys[pygame.K_4]:
            return 4



