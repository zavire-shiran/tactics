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

pygame.init()

size = 640,480

screen.init(size, False)

movingscreen = False

lastframe = pygame.time.get_ticks()
board.init()

while 1:
        for e in pygame.event.get():
                if e.type == pygame.QUIT or \
                   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        sys.exit(0)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 3:
                                movingscreen = True
                                continue
                elif e.type == pygame.MOUSEBUTTONUP:
                        movingscreen = False
                elif board.initialized and movingscreen and e.type == pygame.MOUSEMOTION:
                        board.movemap((-float(e.rel[0])/size[1], -float(e.rel[1])/size[1]))
	dt = (pygame.time.get_ticks() - lastframe)/1000.0
	lastframe = pygame.time.get_ticks()
	for a in texture.animations:
		a.tick(dt)
        screen.startframe()
        if board.initialized:
                board.draw()
        screen.endframe()
        pygame.time.wait(1)
