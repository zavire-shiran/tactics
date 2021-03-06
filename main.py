#!/usr/bin/python
from pygame import display, OPENGL, DOUBLEBUF
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import math
import sys

import screen
import board
import texture
import gui

import editor
import game

keydown = None
mousedown = None

def seteditor():
        global mousedown, keydown
        mousedown, keydown = editor.mousedown, editor.keydown
        board.init(loadfrom = 'map/example')
        editor.register()

def setneweditor():
        global mousedown, keydown
        mousedown, keydown = editor.mousedown, editor.keydown
        board.init()
        editor.register()

def setgame():
        global mousedown, keydown
        mousedown, keydown = game.mousedown, game.keydown
        board.init(loadfrom = 'map/example')
        game.register()

pygame.init()

size = 640,480

screen.init(size, False)

gui.drawfont = 'Arial.ttf'

mainmenuspec = [0.8, 0.35,
		["$logo.png", 0.0, 0, 0.3],
                ["@Play map", 0.0, 0.3, 0.05],
                ["@Edit map", 0.27, 0.3, 0.05],
                ["@Edit new map", 0.53, 0.3, 0.05]]

gui.newwindow(mainmenuspec, None, (.25, .325), [setgame, seteditor, setneweditor])

movingwindow = None
movingscreen = False

lastframe = pygame.time.get_ticks()

while 1:
        for e in pygame.event.get():
                if e.type == pygame.QUIT or \
                   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        sys.exit(0)
                elif e.type == pygame.KEYDOWN and keydown:
                        keydown(pygame.key.name(e.key))
                elif e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 3:
                                movingscreen = True
                                continue
                        point = (float(e.pos[0]) / size[1], float(e.pos[1]) / size[1])
                        inwindow = False
                        for win in gui.windows:
                                if win.click(point):
                                        inwindow = True
                                elif win.ispointin(point):
                                        inwindow = True
                                        movingwindow = win
                        if not inwindow and board.initialized:
                                mousedown(e.button, point)
                elif e.type == pygame.MOUSEBUTTONUP:
                        movingscreen = False
                        movingwindow = None
                elif movingwindow and e.type == pygame.MOUSEMOTION:
                        movingwindow.move((float(e.rel[0])/size[1], float(e.rel[1])/size[1]))
                elif board.initialized and movingscreen and e.type == pygame.MOUSEMOTION:
                        board.movemap((-float(e.rel[0])/size[1], -float(e.rel[1])/size[1]))
	dt = (pygame.time.get_ticks() - lastframe)/1000.0
	lastframe = pygame.time.get_ticks()
	for a in texture.animations:
		a.tick(dt)
	if board.initialized:
		board.advtime()
        screen.startframe()
        if board.initialized:
                board.draw()
        for win in gui.windows:
                win.draw()
        screen.endframe()
        pygame.time.wait(1)
