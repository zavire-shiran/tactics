import sys
import os
import re
import pygame
import gui

import board
import texture

from media import loadtexture

b = None
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

def register():
    global b, images, imagenames, mapname
    font = pygame.font.Font("Arial.ttf", 18)
    b = board.board()
    mapname = filter(optionp, sys.argv)
    if len(mapname) > 1:
        b.load(mapname[1])
    imagenames = filter(lambda s: re.match('.*\.png', s), os.listdir('terrain'))
    images = map(loadtexture, imagenames)
    terrains = os.listdir('terrain')
    ysize = len(terrains) * 0.035 + 0.01
    spec = [['@'+n.split('.')[0], 0.005, i*0.035+0.005, 0.035] for i, n in enumerate(terrains)]
    funcs = [functor(setterrainbrush, loadtexture(n), n.split('.')[0]) for n in terrains]
    window = gui.newwindow([0.25, ysize] + spec, None, (0.0, 0.0), funcs)
    return b

def keydown(key):
    global terrainbrush, entitybrush, brushname
    if key == 'p':
        b.toggleshowpassable()
        if b.showpassable:
            terrainbrush = None
            entitybrush = None
            brushname = "Passability"
        elif brushname == "Passability":
            brushname = ""

def mousedown(button, (x, y)):
    global b
    if button == 1:
        if b.showpassable and brushname == "Passability":
            b.board.reference(b.screentoworld((x,y))).togglepassable()
        if terrainbrush:
            b.board.reference(b.screentoworld((x,y))).texture = terrainbrush
        if entitybrush:
            b.board.reference(b.screentoworld((x,y))).contents = entitybrush()
    elif button == 3 and x < 1.0:
        b.movemap((x - 0.5, y - 0.5))
