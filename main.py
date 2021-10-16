from game import *


if __name__ == '__main__':
  print("Choose player O [HUMAN | AI_EASY | AI_HARD]: ", end='')
  p_o = input()

  print("Choose player X [HUMAN | AI_EASY | AI_HARD]: ", end='')
  p_x = input()


  if "HUMAN" in p_o:      p_o = Player.HUMAN
  elif "AI_EASY" in p_o:  p_o = Player.AI_EASY
  elif "AI_HARD" in p_o:  p_o = Player.AI_HARD
  else:                   p_o = Player.HUMAN

  if "HUMAN" in p_x:      p_x = Player.HUMAN
  elif "AI_EASY" in p_x:  p_x = Player.AI_EASY
  elif "AI_HARD" in p_x:  p_x = Player.AI_HARD
  else:                   p_x = Player.HUMAN


  depth = None
  if Player.AI_HARD in [p_o, p_x]:
    print("Choose max algorithm depth (higher value equals more effective algorithm): ", end='')
    try:
      depth = int(input())
    except ValueError:
      depth = None


  game = Game(player_o = p_o, player_x = p_x)
  if depth is not None: game.minimax_depth = depth


  while True:
    game.start(starts = Symbol.O)
    q = input("Continue playing? [Y/N]: ")
    if q in ["Y", "y"]: continue
    else:               break