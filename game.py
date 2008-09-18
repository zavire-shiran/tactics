import sys
import pygame
import board
import gui

# game state vars
side = 0
statuswindow = None
movewindow = None

menuwindowspec = []

statuswindowspec = [0.32, 0.19,
                    ['**name', 0.005, 0.0, 0.05],
                    ['PA', 0.005, 0.05, 0.035],
                    ['**pa', 0.055, 0.05, 0.035],
                    ['PD', 0.005, 0.085, 0.035],
                    ['**pd', 0.055, 0.085, 0.035],
                    ['SP', 0.11, 0.05, 0.035],
                    ['**sp', 0.165, 0.05, 0.035],
                    ['SR', 0.11, 0.085, 0.035],
                    ['**sr', 0.165, 0.085, 0.035],
                    ['HP', 0.005, 0.12, 0.035],
                    ['**hp', 0.055, 0.12, 0.035],
                    ['TP', 0.11, 0.12, 0.035],
                    ['**tp', 0.165, 0.12, 0.035],
                    ['SPD', 0.005, 0.155, 0.035],
                    ['**speed', 0.07, 0.155, 0.035],
                    ['Move', 0.13, 0.155, 0.035],
                    ['**move', 0.210, 0.155, 0.035],
                    ['@Move', 0.210, 0.05, 0.035]]

def optionp(string):
    return string[0] != '-'

def register():
    gui.removeallwindows()

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
            statuswindow = gui.newwindow(statuswindowspec, board.getselectedcontents(),
                                         pos, [lambda:board.startmove()])
    elif button == 3:
        board.movemap((x - 0.666, y - 0.5))
