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

screen.init(size, False)

b = board.board()
font = pygame.font.Font("Arial.ttf", 18)

move = texture.Text("Moving", font)
notmove = texture.Text("Not Moving", font)
moving = False

def startmove():
	global b, moving
	if moving:
		moving = False
		b.clearmarks()
	elif b.markmove():
		moving = True

while 1:
	for e in pygame.event.get():
		if e.type == pygame.QUIT or \
		   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			sys.exit(0)
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_m:
			startmove()
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_p:
			b.toggleshowpassable()
		elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
			clickpos = (float(e.pos[0]) / size[1],
				    float(e.pos[1]) / size[1])
			if e.pos[0] > size[1] and e.pos[1] > 0.75:
				startmove()
			if moving:
				if e.pos[0] < size[1] and b.move(b.screentoworld(clickpos)):
					moving = False
			elif e.pos[0] < size[1]:
				b.select(clickpos)
		elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
			b.movemap(((float(e.pos[0]) / size[1]) - 0.5, \
				   (float(e.pos[1]) / size[1]) - 0.5))
	screen.startframe()
	b.draw()
	glDisable(GL_TEXTURE_2D)
	glBegin(GL_QUADS)
	glColor4f(0.1, 0.1, 0.3, 1.0)
	glVertex3f(1, 0, 5.0)
	glVertex3f(4.0/3.0, 0, 5.0)
	glVertex3f(4.0/3.0, 1, 5.0)
	glVertex3f(1.0, 1.0, 5.0)
	glEnd()
	glPushMatrix()
	glTranslate(0.0, 0.0, 6.0)
	sel = b.getselected()
	if sel and sel.contents:
		t = texture.Text(str(sel.contents), font)
	else:
		t = texture.Text("None Selected", font)
	t.render((1.01, 0.0), 0.05)
	if moving:
		move.render((1.01, 0.07), 0.05)
	else:
		notmove.render((1.01, 0.07) , 0.05)
	glPopMatrix()
	screen.endframe()
	pygame.time.wait(1)
