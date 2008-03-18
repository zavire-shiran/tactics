import sys
import os
import re
import pygame

import board
import sidebar
import texture

s = None
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
    global b, s, images, imagenames, mapname
    font = pygame.font.Font("Arial.ttf", 18)
    mapname = filter(optionp, sys.argv)[1]
    b = board.board()
    b.load(mapname)
    s = sidebar.sidebar(font)
    imagenames = filter(lambda s: re.match('.*\.png', s), os.listdir('.'))
    images = map(texture.Texture, imagenames)
    redosidebar()
    return b, s

def redosidebar():
    global b, s
    s.clearcontents()
    sel = b.getselected()
    if brushname:
        s.addtext(brushname, 0.06, 0.01)
    else:
        s.addspacer(0.07)
    for imagename, image in zip(imagenames, images):
        iname = imagename
        s.addbutton(imagename, 0.05, 0.01, functor(setterrainbrush, image, imagename))
    s.addspacer(0.07)
    s.addbutton("Hero", 0.05, 0.01, functor(setentitybrush, lambda: board.character(texture.Texture("Hero.png"), "Hero"), "Hero"))
    s.addbutton("Enemy", 0.05, 0.01, 
                functor(setentitybrush, lambda: board.character(texture.Texture("Enemy.png"), "Enemy"), "Enemy"))
    s.addbutton("Empty", 0.05, 0.01, functor(setentitybrush, lambda: None, "Empty"))
    s.addspacer(0.07)
    s.addbutton("Save", 0.05, 0.01, functor(b.save, mapname))

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
        redosidebar()

def mousedown(button, (x, y)):
    global b
    if button == 1:
        if x > 1.0:
            s.click(y)
            redosidebar()
        else:
            if b.showpassable and brushname == "Passability":
                b.board.reference(b.screentoworld((x,y))).togglepassable()
            if terrainbrush:
                b.board.reference(b.screentoworld((x,y))).texture = terrainbrush
            if entitybrush:
                b.board.reference(b.screentoworld((x,y))).contents = entitybrush()
    elif button == 3 and x < 1.0:
        b.movemap((x - 0.5, y - 0.5))
        redosidebar()
