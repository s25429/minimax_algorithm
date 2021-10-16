from enum import IntEnum

class Player(IntEnum):
  HUMAN =   0
  AI_EASY = 1
  AI_HARD = 2

class Symbol(IntEnum):
  O = -1
  X = 1

  def char(self):
    return 'X' if self.value == 1 else 'O'