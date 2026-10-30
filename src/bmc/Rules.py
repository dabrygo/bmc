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


class MemorizeKP(Sequence):
  def __init__(self, material):
    self._material = material

  def verses(self):
    # TODO Break into chunks of 5s and 10s
    # 1, 2, 1-2, 1-2-2-1, 3, 1-2-3, 1-2-3-3-2-1, 4, 1-2-3-4, 1-2-3-4-4-3-2-1, 5, 1-2-3-4-5, 1-2-3-4-5-5-4-3-2-1
    # 6, 7, 6-7, 6-7-7-6, 8, 6-7-8, 6-7-8-8-7-6, 9, 6-7-8-9, 6-7-8-9-9-8-7-6, 10, 6-7-8-9-10, 6-7-8-9-10-10-9-8-7-6
    # 1-2-3-4-5-6-7-8-9-10
    # 11, 12, 11-12, 11-12-12-11, 13, 11-12-13, 11-12-13-13-12-11, 14, 11-12-13-14, 11-12-13-14-14-13-12-11, 15, 11-12-13-14-15, 11-12-13-14-15-15-14-13-12-11
    # 16, 17, 16-17, 16-17-17-16, 18, 16-17-18, 16-17-18-18-17-16, 19, 16-17-18-19, 16-17-18-19-19-18-17-16, 20, 16-17-18-19-20, 16-17-18-19-20-20-19-18-17-16
    # 11-12-13-14-15-16-17-18-19-20
    # 1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20
    sequence = []
    n = len(self._material)
    # n_chunks = n // 5
    for i in range(1, n + 1):
      sequence.append(self._material[i - 1])
      for j in range(1, i + 1):
        sequence.append(self._material[j - 1])
      for j in range(i, 0, -1):
        sequence.append(self._material[j - 1])
    for i in range(n):
      sequence.append(self._material[i])
    return sequence


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
      reordered_material = sequence_file.verses()
    elif sequence == 'sequential':
      reordered_material = Sequential(material).verses()
    elif sequence == 'reverse':
      reordered_material = Reverse(material).verses()
    elif sequence == 'random':
      reordered_material = Random(material).verses()
    elif sequence == 'memorize_kp':
      reordered_material = MemorizeKP(material).verses()
    else:
      assert False, f"Unknown sequence code: {sequence}"
    # Update is redundant if custom
    sequence_file.update_file(reordered_material)
    sequence_file.archive_file(start_time)
    return reordered_material
     
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



