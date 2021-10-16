def is_win(board, symbol):
  """
  This way of calculating wins is purely so it looks nice. It is not fast and could be done faster using less python hacky methods and such. But it looks nice!"""

  matches = [ # Win checks in tic tac toe
    board[0:3],    # [0 1 2]
    board[3:6],    # [3 4 5]
    board[6:9],    # [6 7 8]
    board[0:7:3],  # [0 3 6]
    board[1:8:3],  # [1 4 7]
    board[2:9:3],  # [2 5 8]
    board[0:9:4],  # [0 4 8]
    board[2:7:2],  # [2 4 6]
  ]

  for line in matches:
    if all(symbol == i for i in line): 
      return True

  return False


def is_tie(board):
  return not get_empties(board)


def get_empties(board):
  return [i for i, v in enumerate(board) if v == 0]


def minimax(board: list[int], depth: int, is_maximizing: bool, first: bool = True) -> int:
  """Minimax algorithm based on recursion"""
  if depth == 0:
    return 0

  # Get dictionary of moves:scores and most edge value variable
  moves = {i:0 for i, v in enumerate(board) if v == 0}
  edge_value = float('-inf') if is_maximizing else float('inf')

  for k in moves.copy().keys():
    symbol = 1 if is_maximizing else -1
    new_board = board.copy()
    new_board[k] = symbol
    # print(new_board, '| Moved:', symbol, 'to index:', k) # For debug

    # Calculate score of the currently processed move
    score = 0
    if is_win(new_board, symbol):
      score = symbol * ((len(get_empties(new_board))) + 1)
    elif is_tie(new_board):
      score = 0
    else:
      score = minimax(new_board, depth - 1, not is_maximizing, False)

    # For maximizing we find max, for minimizing - min
    if is_maximizing: edge_value = max(score, edge_value)
    else:             edge_value = min(score, edge_value)
    moves.update({k:score})
    
  # print('Final value:', edge_value, is_maximizing, end='\n') # For debug
  if not first:
    return edge_value

  # If it's first call then we return index of the move we should make
  moves_sorted = {k: v for k, v in sorted(moves.items(), key=lambda x: x[1])}
  if is_maximizing: # Returns key with max value
    return list(moves_sorted.keys())[::-1][0]
  else: # Returns key with min value
    return list(moves_sorted.keys())[0]


if __name__ == '__main__':
  """To test the algorith run this file"""
  board = [
    1, -1, 1, 
    1, -1, 0, 
    0, 0, -1, 
  ]

  print(minimax(board, depth=10, is_maximizing=True))