from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import texture

class staticstring:
    def __init__(self, text, height, linegap):
        self.text = text
        self.height = height
        self.linegap = linegap
    def size(self):
        return self.height + self.linegap
    def draw(self, font, pos):
        t = texture.Text(self.text, font)
        t.render((1.01, pos), self.height)
    def click(self):
        pass

class spacer:
    def __init__(self, space):
        self.space = space
    def size (self):
        return self.space
    def draw(self, font, pos):
        pass
    def click(self):
        pass

class button:
    def __init__(self, text, height, linegap, action):
        self.text = text
        self.height = height
        self.linegap = linegap
        self.action = action
    def draw(self, font, pos):
        t = texture.Text(self.text, font)
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_LINE_LOOP)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glVertex3f(1.01, pos, 1.0)
        glVertex3f(1.33, pos, 1.0)
        glVertex3f(1.33, pos+self.height+self.linegap, 1.0)
        glVertex3f(1.01, pos+self.height+self.linegap, 1.0)
        glEnd()
        t.render((1.01, pos+self.linegap/2), self.height)
    def click(self):
        self.action()
    def size(self):
        return self.height + self.linegap

class sidebar:
    def __init__(self, font):
        self.font = font
        self.clearcontents()
    def clearcontents(self):
        self.contents = []
    def addtext(self, text, height, linegap):
        self.contents.append(staticstring(text, height, linegap))
    def addspacer(self, space):
        self.contents.append(spacer(space))
    def addbutton(self, text, height, linegap, action):
        self.contents.append(button(text, height, linegap, action))
    def click(self, ypos):
        y = 0.0
        for item in self.contents:
            if y + item.size() > ypos:
                return item.click()
            y += item.size()
    def draw(self):
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
        drawpos = 0.0
        for item in self.contents:
            item.draw(self.font, drawpos)
            drawpos += item.size()
	glPopMatrix()
