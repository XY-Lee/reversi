import random
import os
import time
import pygame

SEARCH_DIRECTIONS = [[-1, -1], [0, -1], [1, -1],
                     [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]


class Reversi:
  def __init__(self):
    self.board = [[' ' for i in range(8)] for j in range(8)]
    self.board[3][3] = 'O'
    self.board[4][4] = 'O'
    self.board[3][4] = 'X'
    self.board[4][3] = 'X'

  def print(self):
    # clean screen
    os.system('cls' if os.name == 'nt' else 'clear')

    nRow = len(self.board)
    nCol = len(self.board[0])

    print('  ', end='')
    for i in range(nCol):
      print(str(i), end='')
    print()
    print(' +--------+')
    for i in range(nRow):
      print(str(i) + '|', end='')
      for j in range(nCol):
        print(self.board[i][j], end='')
      print('|')
    print(' +--------+')

  def __isOnBoard(self, r, c):
    return r >= 0 and r < 8 and c >= 0 and c < 8

  def isValidMove(self, tile, r, c):
    r = int(r)
    c = int(c)
    if not self.__isOnBoard(r, c) or self.board[r][c] != ' ':
      return False
    otherTile = 'O' if tile == 'X' else 'X'
    tilesToFlip = []
    for rd, cd in SEARCH_DIRECTIONS:
      rm, cm = r, c
      rm += rd
      cm += cd
      while self.__isOnBoard(rm, cm) and self.board[rm][cm] == otherTile:
        rm += rd
        cm += cd
        if self.__isOnBoard(rm, cm) and self.board[rm][cm] == tile:
          while True:
            rm -= rd
            cm -= cd
            if r == rm and c == cm:
              break
            tilesToFlip.append([rm, cm])
    if len(tilesToFlip) == 0:
      return False
    return tilesToFlip

  def getTips(self, tile):
    tips = []
    for r in range(8):
      for c in range(8):
        hasTip = reversi.isValidMove(tile, r, c)
        if hasTip:
          tips.append([r, c])
    return tips

  def makeMove(self, r, c, tile):
    tilesToFlip = self.isValidMove(tile, r, c)
    if tilesToFlip == False:
      return False
    self.board[r][c] = tile
    for i, j in tilesToFlip:
      self.board[i][j] = tile
    return True

  def getScroe(self):
    play1 = 0
    play2 = 0
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == 'X':
          play1 += 1
        elif self.board[i][j] == 'O':
          play2 += 1
    return {'X': play1, 'O': play2}


# current = 'O'
# reversi = Reversi()
# reversi.print()
# while True:
#     if len(reversi.getTips(current)) == 0:
#         break
#     if current == 'X':
#         print(current + ' ' + str(reversi.getTips(current)))
#         r, c = input().split(',')
#         r = int(r)
#         c = int(c)
#         if reversi.isValidMove(current, r, c):
#             reversi.makeMove(r, c, current)
#             current = 'X' if current == 'O' else 'O'
#     else:
#         time.sleep(0.3)
#         tips = reversi.getTips(current)
#         random.shuffle( tips )
#         computerMove = tips[0]
#         for loc in tips:
#             if len(reversi.isValidMove(current, computerMove[0], computerMove[1])) < len(reversi.isValidMove(current, loc[0], loc[1])) :
#                 computerMove = loc
#         reversi.makeMove(computerMove[0], computerMove[1], current)
#         current = 'X' if current == 'O' else 'O'
#     reversi.print()

# Define some colors
BLACK = (77, 51, 0)
WHITE = (204, 136, 0)
RED = (255, 200, 0)
WIN_COLOR = (175, 175, 0)
LOSE_COLOR = (0, 102, 255)
TIP_COLOR = (255, 0, 255)


# 格子數
nRow = 8
nCol = 8

# This sets the margin between each cell
MARGIN = 5

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 60
HEIGHT = 60

# Initialize pygame
pygame.init()
pygame.mixer.init()
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(MARGIN + WIDTH) * nCol + MARGIN,
               (MARGIN + HEIGHT) * nRow + MARGIN + 60]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Loop until the user clicks the close button.
done = False
gameLock = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# background music
pygame.mixer.music.load('BGM.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)

win = pygame.mixer.Sound('win.wav')
lose = pygame.mixer.Sound('lose.wav')
down = pygame.mixer.Sound('down.wav')

# Set title of screen
pygame.display.set_caption("神秘黑黑白棋")
current = 'X' if random.randint(0, 100) % 2 == 1 else 'O'
canChange = False  # can change user
hasFreeArea = False  # game not end
reversi = Reversi()
reversi.print()
# -------- Main Program Loop -----------
while not done:
  if current == 'X':
    for event in pygame.event.get():  # User did something
      if event.type == pygame.QUIT:  # If user clicked close
        done = True  # Flag that we are done so we exit this loop
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if gameLock:
          done = True
        # User clicks the mouse. Get the position
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)
        # Set that location to one
        print("Click ", pos, "Grid coordinates: ", row, column)
        move = (row, column)
        if reversi.isValidMove(current, move[0], move[1]):
          reversi.makeMove(move[0], move[1], current)
          down.play()
          canChange = True

  if current == 'O':
    tips = reversi.getTips(current)
    time.sleep(0.3 + 0.05*len(tips))
    # random.shuffle(tips)
    if len(tips) > 0:
      computerMove = tips[0]
      for loc in tips:
        if len(reversi.isValidMove(current, computerMove[0], computerMove[1])) < len(reversi.isValidMove(current, loc[0], loc[1])):
          computerMove = loc
      reversi.makeMove(computerMove[0], computerMove[1], current)
      down.play()
    canChange = True

  if done:
    break
  if not gameLock:
    if current == 'X' and not canChange:
      userTips = reversi.getTips('X')
    else:
      userTips = []
    # Set the screen background
    screen.fill(BLACK)
    # font data
    font = pygame.font.SysFont('Consoles', WIDTH + 5)
    # Draw the grid
    hasFreeArea = len(reversi.getTips('X')) != 0 or len(
        reversi.getTips('O')) != 0
    for row in range(nRow):
      for column in range(nCol):
        if [row, column] in userTips:
          color = RED
        else:
          color = WHITE
        pygame.draw.rect(screen,
                         color,
                         [(MARGIN + WIDTH) * column + MARGIN,
                          (MARGIN + HEIGHT) * row + MARGIN,
                          WIDTH,
                          HEIGHT])
        if reversi.board[row][column] == 'X':
          color = (0, 0, 0)
          pygame.draw.circle(screen, color, [(MARGIN + WIDTH) * column + MARGIN + int(WIDTH / 2),
                                             (MARGIN + HEIGHT) * row + MARGIN + int(HEIGHT / 2)], int(HEIGHT / 2))
        elif reversi.board[row][column] == 'O':
          color = (255, 255, 255)
          pygame.draw.circle(screen, color, [(MARGIN + WIDTH) * column + MARGIN + int(WIDTH / 2),
                                             (MARGIN + HEIGHT) * row + MARGIN + int(HEIGHT / 2)], int(HEIGHT / 2))
    pygame.draw.rect(screen,
                     (154, 205, 154),
                     [0,
                      WINDOW_SIZE[1] - 60,
                      (MARGIN + WIDTH) * nCol + MARGIN,
                      60])
    pygame.draw.circle(screen, (0, 0, 0), [0 + int(HEIGHT / 2),
                                           WINDOW_SIZE[1] - 30], int(HEIGHT / 3))
    pygame.draw.circle(screen, (255, 255, 255), [int(WINDOW_SIZE[1]/2),
                                                 WINDOW_SIZE[1] - 30], int(HEIGHT / 3))
    score = reversi.getScroe()
    text = font.render(':{}'.format(score['X']), True, (0, 0, 0))
    screen.blit(text, (0 + int(HEIGHT / 2) * 2, WINDOW_SIZE[1] - 50))
    text = font.render(':{}'.format(score['O']), True, (0, 0, 0))
    screen.blit(text, (int(WINDOW_SIZE[1]/2) +
                       int(HEIGHT / 2), WINDOW_SIZE[1] - 50))

    # change user
    if canChange:
      current = 'X' if current == 'O' else 'O'
      canChange = False
    if not hasFreeArea:
      score = reversi.getScroe()
      if score['X'] > score['O']:
        font = pygame.font.SysFont('Consoles', WIDTH + 50)
        text = font.render('you win', True, WIN_COLOR)
        screen.blit(text, (10, 10))
        text = font.render('click to leave', True, TIP_COLOR)
        screen.blit(text, (20, 60))
        pygame.mixer.music.stop()
        win.play(1)
      elif score['X'] < score['O']:
        font = pygame.font.SysFont('Consoles', WIDTH + 50)
        text = font.render('you lose', True, LOSE_COLOR)
        screen.blit(text, (10, 10))
        text = font.render('click to leave', True, TIP_COLOR)
        screen.blit(text, (20, 60))
        pygame.mixer.music.stop()
        lose.play(1)
      else:
        font = pygame.font.SysFont('Consoles', WIDTH + 50)
        text = font.render('The game ended in a draw.', True, LOSE_COLOR)
        screen.blit(text, (10, 10))
        text = font.render('click to leave', True, TIP_COLOR)
        screen.blit(text, (20, 60))
      gameLock = True

  # Limit to 60 frames per second
  clock.tick(60)

  # Go ahead and update the screen with what we've drawn.
  pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

score = reversi.getScroe()
print("you : {0}   computer : {1}".format(score['X'], score['O']))
