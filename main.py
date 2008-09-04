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

b = register()
gui.drawfont = pygame.font.Font("Arial.ttf", 18)

movingwindow = None
movingscreen = False

while 1:
	for e in pygame.event.get():
		if e.type == pygame.QUIT or \
		   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			sys.exit(0)
		elif e.type == pygame.KEYDOWN:
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
			if not inwindow:
				mousedown(e.button, point)
		elif e.type == pygame.MOUSEBUTTONUP:
			movingscreen = False
			movingwindow = None
		elif movingwindow and e.type == pygame.MOUSEMOTION:
			movingwindow.move((float(e.rel[0])/size[1], float(e.rel[1])/size[1]))
		elif movingscreen and e.type == pygame.MOUSEMOTION:
			b.movemap((-float(e.rel[0])/size[1], -float(e.rel[1])/size[1]))
	screen.startframe()
	b.draw()
	for win in gui.windows:
		win.draw()
	screen.endframe()
	pygame.time.wait(1)
