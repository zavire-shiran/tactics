import sys
import os
import re
import pygame
import gui

import board
import texture
import chars

from media import loadtexture

terrainbrush = None
entitybrush = None
brushname = None
imagenames = None
images = None

mapname = None

def functor(func, *args):
    return lambda: func(*args)

def setterrainbrush(image, imagename):
    global terrainbrush, brushname, entitybrush
    entitybrush = None
    terrainbrush = image
    brushname = imagename

def setentitybrush(entitygen, entityname):
    global entitybrush, terrainbrush, brushname
    terrainbrush = None
    entitybrush = entitygen
    brushname = entityname

def optionp(string):
    return string[0] != '-'

def makeeditwindow():
    global window
    terrains = os.listdir('terrain')
    terrainysize = len(terrains) * 0.035
    spec = [['@'+n.split('.')[0], 0.005, i*0.035+0.005, 0.035] for i, n in enumerate(terrains)]
    charspec = [['@Add Char', 0.005, terrainysize, 0.035], ['@Rem Char', 0.005, terrainysize+0.035, 0.035]]
    funcs = [functor(setterrainbrush, loadtexture(n), n.split('.')[0]) for n in terrains] + \
            [functor(setentitybrush, addchar, 'add char'), functor(setentitybrush, remchar, 'remchar')]
    window = gui.newwindow([0.25, terrainysize + 0.08] + spec + charspec, None, (0.0, 0.0), funcs)

def register():
    global images, imagenames, mapname
    gui.removeallwindows()
    font = pygame.font.Font("Arial.ttf", 18)
    makeeditwindow()

def addchar():
    return chars.character(loadtexture('Hero.png'), 'Name')

def remchar():
    return None

def keydown(key):
    global terrainbrush, entitybrush, brushname
    if key == 'p':
        board.toggleshowpassable()
        if board.showpassable:
            terrainbrush = None
            entitybrush = None
            brushname = "Passability"
        elif brushname == "Passability":
            brushname = ""

def mousedown(button, (x, y)):
    if button == 1:
        if board.showpassable and brushname == "Passability":
            board.board.reference(board.screentoworld((x,y))).togglepassable()
        if terrainbrush:
            board.board.reference(board.screentoworld((x,y))).texture = terrainbrush
        if entitybrush:
            board.board.reference(board.screentoworld((x,y))).contents = entitybrush()
    elif button == 3 and x < 1.0:
        board.movemap((x - 0.5, y - 0.5))
