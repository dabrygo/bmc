'''Palette of hues'''
import abc


class Color(abc.ABC):
  @abc.abstractmethod
  def rgb(self):
    pass


class White(abc.ABC):
  def rgb(self):
    return (255, 255, 255)


class Black(abc.ABC):
  def rgb(self):
    return (0, 0, 0)
