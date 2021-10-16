from dataclasses import dataclass, field
from random import choice
from time import sleep
from enums import *


@dataclass
class Game:
  player_o: Player =    field(default=Player.HUMAN)
  player_x: Player =    field(default=Player.AI_EASY)
  board: list =         field(init=False, default_factory=list)
  minimax_depth: int =  field(init=False, default=10)

  def __post_init__(self):
    self.board = [0 for _ in range(9)]


  def start(self, starts: Symbol = Symbol.O):
    """Runs game itself"""
    if len(self.get_possible_moves()) != 9:
      self.board = [0 for _ in range(9)]

    curr_symbol = starts
    curr_player = self.update_player(curr_symbol)


    while curr_player is not None:
      if self.is_tie():
        print(f"\nIt's a tie!")
        self.print()
        break

      self.print()
      print(f"<{curr_symbol.char()}> Choose square: ", end='')

      chosen = self.get_input(curr_player, curr_symbol)
      print(f"Player {curr_symbol.char()} chose square {chosen}")

      self.set_move(chosen, curr_symbol)

      if self.is_won(curr_symbol):
        print(f"\nPlayer {curr_symbol.char()} wins!")
        self.print()
        break

      curr_symbol = self.update_symbol(curr_symbol)
      curr_player = self.update_player(curr_symbol)


  def update_symbol(self, symbol: Symbol) -> Symbol:
    """Returns other symbol based on given one"""
    return Symbol.O if symbol == Symbol.X else Symbol.X

  def update_player(self, symbol: Symbol) -> Player:
    """Returns proper player based on given symbol"""
    if   symbol == Symbol.O: return self.player_o
    elif symbol == Symbol.X: return self.player_x
    else:                    return None


  def set_move(self, index: int, symbol: Symbol):
    """Sets move onto the board"""
    self.board[index] = symbol.value

  def get_possible_moves(self, board = None) -> list[int]:
    """Returns list of possible moves"""
    return [i for i, v in enumerate(self.board if board is None else board) if v == 0]

  def get_input(self, player: Player, symbol: Symbol) -> int:
    """Returns a choice of square based on type of player"""
    if player == Player.HUMAN:
      while True:
        try:
          chosen = int(input())
          if chosen not in self.get_possible_moves(): 
            raise ValueError
          return chosen
        except ValueError:
          print("Choose a valid square: ", end='')
          continue
    else:
      return self.ai_move(player, symbol)


  def ai_move(self, player: Player, symbol: Symbol) -> int:
    if player == Player.AI_EASY:
      print()
      return self.random_choice()
    
    else:
      if len(self.get_possible_moves()) == 9:
        return self.random_choice()
      is_maximizing = True if symbol.value == 1 else False
      return self.minimax(self.board, self.minimax_depth, is_maximizing)


  def random_choice(self) -> int:
    sleep(1)
    return choice(self.get_possible_moves())


  def minimax(self, board: list[int], depth: int, is_maximizing: bool, first: bool = True) -> int:
    """Minimax algorithm for hard ai"""
    if depth == 0:
      return 0

    # Get dictionary of moves:scores and most edge value variable
    moves = {i:0 for i, v in enumerate(board) if v == 0}
    edge_value = float('-inf') if is_maximizing else float('inf')

    for k in moves.copy().keys():
      symbol = 1 if is_maximizing else -1
      new_board = board.copy()
      new_board[k] = symbol

      # Calculate score of the currently processed move
      score = 0
      if self.is_won(symbol, new_board):
        score = symbol * ((len(self.get_possible_moves(new_board))) + 1)
      elif self.is_tie(new_board):
        score = 0
      else:
        score = self.minimax(new_board, depth - 1, not is_maximizing, False)

      # For maximizing we find max, for minimizing - min
      if is_maximizing: edge_value = max(score, edge_value)
      else:             edge_value = min(score, edge_value)
      moves.update({k:score})
      
    if not first:
      return edge_value

    # If it's first call then we return index of the move we should make
    moves_sorted = {k: v for k, v in sorted(moves.items(), key=lambda x: x[1])}
    if is_maximizing: # Returns key with max value
      return list(moves_sorted.keys())[::-1][0]
    else: # Returns key with min value
      return list(moves_sorted.keys())[0]


  def is_tie(self, board = None) -> int:
    """Return True if there is no possible moves left"""
    return not self.get_possible_moves(board)

  def is_won(self, symbol: Symbol, board = None) -> bool:
    """Returns True if specific symbol has won and False if not.
    This way of calculating wins is purely so it looks nice. It is not fast and could be done faster using less python hacky methods and such. But it looks quite nice."""
    curr_board = self.board if board is None else board
    matches = [ # Win checks in tic tac toe
      curr_board[0:3],    # [0 1 2]
      curr_board[3:6],    # [3 4 5]
      curr_board[6:9],    # [6 7 8]
      curr_board[0:7:3],  # [0 3 6]
      curr_board[1:8:3],  # [1 4 7]
      curr_board[2:9:3],  # [2 5 8]
      curr_board[0:9:4],  # [0 4 8]
      curr_board[2:7:2],  # [2 4 6]
    ]

    for line in matches:
      if all(symbol == i for i in line): 
        return True

    return False


  def to_symbol(self, num: int) -> str:
    """Returns given number to symbol for displaying"""
    if num == 1:    return 'X'
    elif num == -1: return 'O'
    else:           return ' '

  def print(self):
    """Prints board to the screen"""
    s = [self.to_symbol(i) for i in self.board]
    board = """                    ___________
 {0} | {1} | {2}         | 0 | 1 | 2 |
---+---+---        |---+---+---|
 {3} | {4} | {5}         | 3 | 4 | 5 |
---+---+---        |---+---+---|
 {6} | {7} | {8}         |_6_|_7_|_8_|
 [ Board ]""".format(
      s[0], s[1], s[2], 
      s[3], s[4], s[5], 
      s[6], s[7], s[8]
    )
    print(board)
