import sys
import os
import re
import pygame
import gui

import board
import texture
import chars
import media

from media import loadtexture

terrainbrush = None
entitybrush = None
brushname = None
imagenames = None
images = None
editbrush = False

mapname = None

class EditorState:
    def __init__(self):
        self.brushname = None

es = EditorState()

def functor(func, *args):
    return lambda: func(*args)

def setterrainbrush(image, imagename):
    global terrainbrush, brushname, entitybrush, editbrush
    entitybrush = None
    terrainbrush = image
    es.brushname = imagename
    editbrush = False

def setentitybrush(entitygen, entityname):
    global entitybrush, terrainbrush, brushname, editbrush
    terrainbrush = None
    entitybrush = entitygen
    es.brushname = entityname
    editbrush = False

def seteditchar():
    global entitybrush, terrainbrush, brushname, editbrush
    entitybrush = None
    terrainbrush = None
    es.brushname = 'Edit Char'
    editbrush = True

def optionp(string):
    return string[0] != '-'

def makeeditwindow():
    global window
    gui.removeallwindows()
    terrains = [(i[1], i[1][8:]) for i in media.dircontents('terrain')]
    terrainysize = len(terrains) * 0.035
    namespec = ['**brushname', 0.005, 0.005, 0.035]
    spec = [['@'+n[1].split('.')[0], 0.05, i*0.035+0.055, 0.035] for i, n in enumerate(terrains)]
    charspec = [['@Add Char', 0.05, terrainysize+0.065, 0.035],
                ['@Add Enemy', 0.05, terrainysize+0.100, 0.035],
                ['@Rem Char', 0.05, terrainysize+0.135, 0.035],
                ['@Edit Char', 0.05, terrainysize+0.170, 0.035],
                ['@Save map', 0.05, terrainysize+0.215, 0.035]]
    funcs = [functor(setterrainbrush, loadtexture(n[0]), n[1].split('.')[0]) for n in terrains] + \
            [functor(setentitybrush, addchar, 'Add Char'), functor(setentitybrush, addenemy, 'Add Enemy'),
             functor(setentitybrush, remchar, 'Rem Char'), seteditchar, savemap]
    window = gui.newwindow([0.25, terrainysize + 0.255, namespec] + spec + charspec, es, (0.0, 0.0), funcs)

def incstat(character, s):
    character.stats[s] += 1

def decstat(character, s):
    character.stats[s] -= 1

def makecharwindow(character):
    global window
    height = 0.005
    spec = []
    funcs = []
    for k in character.stats.keys():
        spec.append([k, 0.005, height, 0.035])
        spec.append(['@-', 0.125, height, 0.035])
        spec.append(['***stats.'+k, 0.160, height, 0.035])
        spec.append(['@+', 0.255, height, 0.035])
        funcs.append(functor(decstat, character, k))
        funcs.append(functor(incstat, character, k))
        height += 0.035
    spec.append(["@Done", 0.005, height, 0.035])
    funcs.append(makeeditwindow)
    gui.removeallwindows()
    window = gui.newwindow([0.35, len(character.stats.keys()) * 0.035 + 0.050] + spec, character, (0.0, 0.0), funcs)

def register():
    global images, imagenames, mapname
    makeeditwindow()

def addchar():
    return chars.character(loadtexture('Hero.png'), 'Name')

def addenemy():
    return chars.character(loadtexture('Enemy.png'), 'Name')

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
    elif key == '-':
        board.screensize += 1.0
    elif key == '=':
        board.screensize = max(1.0, board.screensize - 1.0)

def mousedown(button, (x, y)):
    if button == 1:
        if board.showpassable and es.brushname == "Passability":
            board.board.reference(board.screentoworld((x,y))).togglepassable()
        if terrainbrush:
            board.board.reference(board.screentoworld((x,y))).texture = terrainbrush
        if entitybrush:
            board.board.reference(board.screentoworld((x,y))).contents = entitybrush()
        if editbrush:
            thing = board.board.reference(board.screentoworld((x,y))).contents
            if thing:
                makecharwindow(thing)
                
    elif button == 3 and x < 1.0:
        board.movemap((x - 0.5, y - 0.5))
