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
import sidebar

pygame.init()

size = 640,480

screen.init(size, False)

font = pygame.font.Font("Arial.ttf", 18)

b = board.board()
s = sidebar.sidebar(font)

noneselected = texture.Text("None Selected", font)
move = texture.Text("Moving", font)
notmove = texture.Text("Not Moving", font)

def redosidebar():
	global b, s
	s.clearcontents()
	sel = b.getselected()
	if sel and sel.contents:
		first = True
		for line in str(sel.contents).split('\n'):
			if first:
				s.addtext(line, 0.06, 0.01)
				first = False
			else:
				s.addtext(line, 0.04, 0.005)
		s.addspacer(0.05)
		if b.moving:
			s.addbutton("Moving", 0.05, 0.01, lambda:b.startmove())
		else:
			s.addbutton("Not Moving", 0.05, 0.01, lambda:b.startmove())

def keydown(key):
	if key == 'm':
		b.startmove()
		redosidebar()
	elif key == 'p':
		b.toggleshowpassable()

def mousedown(button, (x, y)):
	global b
	if button == 1:
		if x > 1.0:
			s.click(y)
			redosidebar()
		else:
			b.select((x,y))
			redosidebar()
	elif button == 3:
		b.movemap((x - 0.5, y - 0.5))
		redosidebar()

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
	s.draw()
	screen.endframe()
	pygame.time.wait(1)

#filter(lambda s: re.match('.*\.png', s), os.listdir('.'))
