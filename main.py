#!/usr/bin/python
from pygame import display, OPENGL, DOUBLEBUF
import pygame
import screen
import math
import sys

pygame.init()

frametime = .05

size = 800, 600

screen.init(size)

try:
	while 1:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				sys.exit(0)
				
		screen.startframe()
		screen.endframe()
		pygame.time.wait(1)


except KeyboardInterrupt:
	pass

