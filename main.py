#!/usr/bin/python
from pygame import display, OPENGL, DOUBLEBUF
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import screen
import board
import texture

import math
import sys

pygame.init()

frametime = .05

size = 640, 480

screen.init(size)

b = board.board()

t = texture.Text("Hello", pygame.font.Font("Arial.ttf", 18))

try:
	while 1:
		for e in pygame.event.get():
			if e.type == pygame.QUIT or \
			   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				sys.exit(0)
			if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
				if not e.pos[0] > size[1]:
					b.select((float(e.pos[0]) / size[1],
						  float(e.pos[1]) / size[1]))
			if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
				b.move(((float(e.pos[0]) / size[1]) - 0.5, \
					(float(e.pos[1]) / size[1]) - 0.5))

		screen.startframe()
		b.draw()
		glDisable(GL_TEXTURE_2D)
		glBegin(GL_QUADS)
		glColor4f(0.1, 0.1, 0.3, 1.0)
		glVertex3f(1, 0, 5)
		glVertex3f(size[0]/float(size[1]), 0, 5)
		glVertex3f(size[0]/float(size[1]), 1, 5)
		glVertex3f(1, 1, 5)
		glEnd()
		glPushMatrix()
		glTranslate(0.0, 0.0, 6.0)
		t.render((1.01, 0.0), 0.075)
		glPopMatrix()
		screen.endframe()
		pygame.time.wait(1)


except KeyboardInterrupt:
	pass
