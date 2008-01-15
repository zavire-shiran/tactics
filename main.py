#!/usr/bin/python
from pygame import display, OPENGL, DOUBLEBUF
from OpenGL.GL import *
from OpenGL.GLU import *
import Image

import pygame
import screen
import board
import texture

import math
import sys

pygame.init()

frametime = .05

size = 800, 600

screen.init(size)

b = board.board(texture.Texture(Image.open("Grass.png")))

pos = [0.0, 0.0]

try:
	while 1:
		for e in pygame.event.get():
			if e.type == pygame.QUIT or \
			e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				sys.exit(0)
			if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
				pos[0] += (float(e.pos[0]) / size[1]) - 0.5
				pos[1] += (float(e.pos[1]) / size[1]) - 0.5

		screen.startframe()
		b.draw(pos)
		screen.endframe()
		pygame.time.wait(1)


except KeyboardInterrupt:
	pass
