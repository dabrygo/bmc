import csv
import os
import random
import sys

import pygame

from bmc import GameView


class Sequence:
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

  def sequenced(self, material):
    '''Choose order to present material to user'''
    sequence = self.sequence()
    if sequence == 'custom':
      sequence_file = Sequence.from_file(material)
      reordered_material = sequence_file.verses()
      return reordered_material
    elif sequence == 'sequential':
      return material
    elif sequence == 'reverse':
      return material[::-1]
    elif sequence == 'random':
      return random.sample(material, len(material))
    assert False, f"Unknown sequence code: {sequence}"

  def sequence(self):
    '''Choose order to present material to user'''
    supported_sequences = ['custom', 'sequential', 'reverse', 'random']
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



