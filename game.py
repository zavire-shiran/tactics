import sys
import pygame
import board
import sidebar
import gui

s = None
b = None

# game state vars
side = 0
statuswindow = None

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
    global b, statuswindow
    if button == 1:
        gui.remwindow(statuswindow)
        pos = (0.95, 0.79)
        if statuswindow:
            pos = statuswindow.pos
        statuswindow = None
        b.select((x,y))
        if b.getselectedcontents():
            statuswindow = gui.newwindow(gui.statuswindowspec, b.getselectedcontents(), pos, (0.32, 0.16))
    elif button == 3:
        b.movemap((x - 0.666, y - 0.5))
