import sys
import pygame
import board
import gui

# game state vars
side = 0
statuswindow = None
movewindow = None

movewindowspec = [0.32, 0.19,
                  ['**name', 0.005, 0.0, 0.05],
                  ['PA', 0.005, 0.05, 0.035],
                  ['***stats.pa', 0.055, 0.05, 0.035],
                  ['PD', 0.005, 0.085, 0.035],
                  ['***stats.pd', 0.055, 0.085, 0.035],
                  ['SP', 0.11, 0.05, 0.035],
                  ['***stats.sp', 0.165, 0.05, 0.035],
                  ['SR', 0.11, 0.085, 0.035],
                  ['***stats.sr', 0.165, 0.085, 0.035],
                  ['HP', 0.005, 0.12, 0.035],
                  ['***stats.hp', 0.055, 0.12, 0.035],
                  ['TP', 0.11, 0.12, 0.035],
                  ['***stats.tp', 0.165, 0.12, 0.035],
                  ['CT', 0.210, 0.12, 0.035],
                  ['***stats.ct', .265, 0.12, 0.035],
                  ['SPD', 0.005, 0.155, 0.035],
                  ['***stats.speed', 0.07, 0.155, 0.035],
                  ['Move', 0.13, 0.155, 0.035],
                  ['***stats.move', 0.210, 0.155, 0.035],
                  ['@Move', 0.210, 0.05, 0.035],
                  ['@Attack', 0.210, 0.084, 0.035]]

statuswindowspec = [0.32, 0.19,
                    ['**name', 0.005, 0.0, 0.05],
                    ['PA', 0.005, 0.05, 0.035],
                    ['***stats.pa', 0.055, 0.05, 0.035],
                    ['PD', 0.005, 0.085, 0.035],
                    ['***stats.pd', 0.055, 0.085, 0.035],
                    ['SP', 0.11, 0.05, 0.035],
                    ['***stats.sp', 0.165, 0.05, 0.035],
                    ['SR', 0.11, 0.085, 0.035],
                    ['***stats.sr', 0.165, 0.085, 0.035],
                    ['HP', 0.005, 0.12, 0.035],
                    ['***stats.hp', 0.055, 0.12, 0.035],
                    ['TP', 0.11, 0.12, 0.035],
                    ['***stats.tp', 0.165, 0.12, 0.035],
                    ['CT', 0.210, 0.12, 0.035],
                    ['***stats.ct', .265, 0.12, 0.035],
                    ['SPD', 0.005, 0.155, 0.035],
                    ['***stats.speed', 0.07, 0.155, 0.035],
                    ['Move', 0.13, 0.155, 0.035],
                    ['***stats.move', 0.210, 0.155, 0.035]]

def optionp(string):
    return string[0] != '-'

def register():
    gui.removeallwindows()

def keydown(key):
    if key == 'm':
        board.startmove()
    elif key == 'p':
        board.toggleshowpassable()
    elif key == '-':
        board.screensize += 1.0
    elif key == '=':
        board.screensize = max(1.0, board.screensize - 1.0)

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
            if board.getselectedcontents().stats['ct'] >= 1.0:
                statuswindow = gui.newwindow(movewindowspec, board.getselectedcontents(),
                                             pos, [lambda:board.startmove(), lambda:board.startattack()])
            else:
                statuswindow = gui.newwindow(statuswindowspec, board.getselectedcontents(),
                                             pos, [])
    elif button == 3:
        board.movemap((x - 0.666, y - 0.5))
