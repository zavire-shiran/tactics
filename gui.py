import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import texture

drawfont = None

windows = []

def newwindow(spec, obj, pos, size):
    windows.append(window(spec, obj, pos[0], pos[1], size[0], size[1]))
    return windows[-1]

def remwindow(win):
    if windows.count(win) > 0:
        windows.remove(win)

statuswindowspec = [['**name', 0.005, 0.0, 0.05],
		    ['ST', 0.005, 0.05, 0.035],
		    ['**str', 0.055, 0.05, 0.035],
		    ['IQ', 0.005, 0.085, 0.035],
		    ['**iq', 0.055, 0.085, 0.035],
		    ['DX', 0.11, 0.05, 0.035],
		    ['**dex', 0.165, 0.05, 0.035],
		    ['HT', 0.11, 0.085, 0.035],
		    ['**ht', 0.165, 0.085, 0.035],
		    ['HP', 0.005, 0.12, 0.035],
		    ['**hp', 0.055, 0.12, 0.035],
		    ['FP', 0.11, 0.12, 0.035],
		    ['**fp', 0.165, 0.12, 0.035]]

class window:
    def __init__(self, spec, character, x, y, xsize, ysize):
        self.char = character
        self.pos = (x, y)
        self.size = (xsize, ysize)
        self.spec = spec
    def ispointin(self, (x, y)):
        return self.pos[0] <= x <= self.pos[0] + self.size[0] and \
               self.pos[1] <= y <= self.pos[1] + self.size[1]
    def move(self, (dx, dy)):
        x, y = self.pos
        self.pos = (x + dx, y + dy)
    def draw(self):
        x, y = self.pos
        xsize, ysize = self.size
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glColor4f(0.1, 0.1, 0.3, 1.0)
        glVertex3f(x, y, 5.0)
        glVertex3f(x+xsize, y, 5.0)
        glVertex3f(x+xsize, y+ysize, 5.0)
        glVertex3f(x, y+ysize, 5.0)
        glEnd()

        glPushMatrix()
        glTranslate(0.0, 0.0, 6.0)
        for s in self.spec:
            if s[0][:2] == '**':
                t = texture.Text(str(getattr(self.char, s[0][2:])), drawfont)
            else:
                t = texture.Text(s[0], drawfont)
            t.render((x+s[1], y+s[2]), s[3])
        glPopMatrix()
