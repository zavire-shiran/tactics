import sys
import pygame
import board
import sidebar

s = None
b = None

# game state vars
side = 0

def optionp(string):
    return string[0] != '-'

def register():
    global b, s, side
    font = pygame.font.Font("Arial.ttf", 18)
    mapname = filter(optionp, sys.argv)[1]
    b = board.board()
    b.load(mapname)
    return b, s

def keydown(key):
    if key == 'm':
        b.startmove()
    elif key == 'p':
        b.toggleshowpassable()

def mousedown(button, (x, y)):
    global b
    if button == 1:
        b.select((x,y))
    elif button == 3:
        b.movemap((x - 0.666, y - 0.5))
