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

if '-e' in sys.argv:
	from editor import register, mousedown, keydown
else:
	from game import register, mousedown, keydown

pygame.init()

size = 640,480

screen.init(size, False)

b, s = register()
sw = gui.statuswindow(None, 0.95, 0.79, 0.32, 0.16)
gui.drawfont = pygame.font.Font("Arial.ttf", 18)

while 1:
	for e in pygame.event.get():
		if e.type == pygame.QUIT or \
		   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			sys.exit(0)
		if e.type == pygame.KEYDOWN:
			keydown(pygame.key.name(e.key))
		elif e.type == pygame.MOUSEBUTTONDOWN:
			mousedown(e.button, (float(e.pos[0]) / size[1], float(e.pos[1]) / size[1]))
	screen.startframe()
	b.draw()
	sw.draw()
	screen.endframe()
	pygame.time.wait(1)
