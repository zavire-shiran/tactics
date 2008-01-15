from pygame import display, OPENGL, DOUBLEBUF, time
from OpenGL.GL import *
from OpenGL.GLU import *
import math


def init(size):
	width, height = size
	surface = display.set_mode(size, OPENGL | DOUBLEBUF)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, 1, 0, 1, 1, -1)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()

	glClearColor(0.1, 0.1, 0.1, 1.0)
	glEnable(GL_DEPTH_TEST)
	glDisable(GL_CULL_FACE)
	
def startframe():
	glLoadIdentity()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def endframe():
	display.flip()

