import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import texture

drawfont = None

windows = []

def newwindow(spec, obj, pos, actions):
    windows.append(window(spec, obj, pos[0], pos[1], actions))
    return windows[-1]

def remwindow(win):
    if windows.count(win) > 0:
        windows.remove(win)

def removeallwindows():
    global windows
    windows = []

class window:
    def __init__(self, spec, character, x, y, actions):
        self.char = character
        self.pos = (x, y)
        self.size = tuple(spec[0:2])
        self.spec = spec[2:]
        self.actions = actions
    def click(self, (x, y)):
        if self.ispointin((x, y)):
            for s in self.spec:
                if s[0][0] == '@' and \
                   self.pos[0]+s[1] <= x <= self.pos[0]+s[1]+texture.horizsize(s[0][1:], drawfont, s[3]) and \
                   self.pos[1]+s[2] <= y <= self.pos[1]+s[2]+s[3]:
                    self.actions[[p[0] for p in self.spec if p[0][0] == '@'].index(s[0])]()
                    return True
        return False
                
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
            elif s[0][:1] == '@':
                t = texture.Text(s[0][1:], drawfont)
                hsize = t.horizsize(s[3])
                glDisable(GL_TEXTURE_2D)
                glBegin(GL_LINE_LOOP)
                glColor4f(1.0, 1.0, 1.0, 1.0)
                glVertex3f(x+s[1]-0.005, y+s[2], 0.01)
                glVertex3f(x+s[1]+hsize+0.005, y+s[2], 0.01)
                glVertex3f(x+s[1]+hsize+0.005, y+s[2]+s[3], 0.01)
                glVertex3f(x+s[1]-0.005, y+s[2]+s[3], 0.01)
                glEnd()
            else:
                t = texture.Text(s[0], drawfont)
            t.render((x+s[1], y+s[2]), s[3])
        glPopMatrix()
