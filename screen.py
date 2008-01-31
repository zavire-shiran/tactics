from pygame import display, OPENGL, DOUBLEBUF, time
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def init(size):
	width, height = size
	surface = display.set_mode(size, OPENGL | DOUBLEBUF)

        glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, float(width)/float(height), 1, 0, -10, 10)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()

	glClearColor(0.9, 0.3, 0.3, 1.0)
	glEnable(GL_DEPTH_TEST)
	glDisable(GL_CULL_FACE)

	return float(width)/height
	
def startframe():
	glLoadIdentity()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def endframe():
	display.flip()
