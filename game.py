import sys
import pygame
import board
import gui

# game state vars
side = 0
statuswindow = None

def optionp(string):
    return string[0] != '-'

def register():
    pass

def keydown(key):
    if key == 'm':
        board.startmove()
    elif key == 'p':
        board.toggleshowpassable()

def mousedown(button, (x, y)):
    global statuswindow
    if button == 1:
        gui.remwindow(statuswindow)
        pos = (0.95, 0.79)
        if statuswindow:
            pos = statuswindow.pos
        statuswindow = None
        board.select((x,y))
        if board.getselectedcontents():
            statuswindow = gui.newwindow(gui.statuswindowspec, board.getselectedcontents(),
                                         pos, [lambda:board.startmove()])
    elif button == 3:
        board.movemap((x - 0.666, y - 0.5))
