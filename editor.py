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

class EditorState:
    def __init__(self):
        self.brushname = None

es = EditorState()

def functor(func, *args):
    return lambda: func(*args)

def setterrainbrush(image, imagename):
    global terrainbrush, brushname, entitybrush
    entitybrush = None
    terrainbrush = image
    es.brushname = imagename

def setentitybrush(entitygen, entityname):
    global entitybrush, terrainbrush, brushname
    terrainbrush = None
    entitybrush = entitygen
    es.brushname = entityname

def optionp(string):
    return string[0] != '-'

def makeeditwindow():
    global window
    terrains = os.listdir('terrain')
    terrainysize = len(terrains) * 0.035
    namespec = ['**brushname', 0.005, 0.005, 0.035]
    spec = [['@'+n.split('.')[0], 0.005, i*0.035+0.055, 0.035] for i, n in enumerate(terrains)]
    charspec = [['@Add Char', 0.005, terrainysize+0.055, 0.035],
                ['@Rem Char', 0.005, terrainysize+0.090, 0.035],
                ['@Save map', 0.005, terrainysize+0.135, 0.035]]
    funcs = [functor(setterrainbrush, loadtexture(n), n.split('.')[0]) for n in terrains] + \
            [functor(setentitybrush, addchar, 'Add Char'), functor(setentitybrush, remchar, 'Rem Char'), savemap]
    window = gui.newwindow([0.25, terrainysize + 0.175, namespec] + spec + charspec, es, (0.0, 0.0), funcs)

def register():
    global images, imagenames, mapname
    gui.removeallwindows()
    font = pygame.font.Font("Arial.ttf", 18)
    makeeditwindow()

def addchar():
    return chars.character(loadtexture('Hero.png'), 'Name')

def remchar():
    return None

def savemap():
    board.save('map/example')

def keydown(key):
    global terrainbrush, entitybrush, brushname
    if key == 'p':
        board.toggleshowpassable()
        if board.showpassable:
            terrainbrush = None
            entitybrush = None
            es.brushname = "Passability"
        elif es.brushname == "Passability":
            es.brushname = ""

def mousedown(button, (x, y)):
    if button == 1:
        if board.showpassable and es.brushname == "Passability":
            board.board.reference(board.screentoworld((x,y))).togglepassable()
        if terrainbrush:
            board.board.reference(board.screentoworld((x,y))).texture = terrainbrush
        if entitybrush:
            board.board.reference(board.screentoworld((x,y))).contents = entitybrush()
    elif button == 3 and x < 1.0:
        board.movemap((x - 0.5, y - 0.5))
