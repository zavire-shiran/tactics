import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import media
import texture
import screen

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
            buttonsonly = [z for z in self.spec if z[0][0] == '@']
            for n,s in enumerate(buttonsonly):
                if self.pos[0]+s[1] <= x <= self.pos[0]+s[1]+texture.horizsize(s[0][1:], drawfont, s[3]) and \
                   self.pos[1]+s[2] <= y <= self.pos[1]+s[2]+s[3]:
                    self.actions[n]()
                    return True
        return False
                
    def ispointin(self, (x, y)):
        return self.pos[0] - 0.01 <= x <= self.pos[0] + self.size[0] + 0.01 and \
               self.pos[1] - 0.01 <= y <= self.pos[1] + self.size[1] + 0.01
    def move(self, (dx, dy)):
        x, y = self.pos
        self.pos = (x + dx, y + dy)
    def draw(self):
        x, y = self.pos
        xsize, ysize = self.size
        bg = media.loadtexture("menu_bg.png")
        corner = media.loadtexture("menu_corner.png")
        vertborder = media.loadtexture("menu_side.png")
        horzborder = media.loadtexture("menu_topbot.png")
        buttonbg = media.loadtexture("menu_buttonbg.png")

        bg()
        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x+xsize, y, 5.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x+xsize, y+ysize, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y+ysize, 5.0)
        glEnd()

        corner()
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x-0.01, y-0.01, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x, y-0.01, 5.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x, y, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x-0.01, y, 5.0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x+xsize, y-0.01, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x+xsize+0.01, y-0.01, 5.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x+xsize+0.01, y, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x+xsize, y, 5.0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x-0.01, y+ysize, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x, y+ysize, 5.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x, y+ysize+0.01, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x-0.01, y+ysize+0.01, 5.0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x+xsize, y+ysize, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x+xsize+0.01, y+ysize, 5.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x+xsize+0.01, y+ysize+0.01, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x+xsize, y+ysize+0.01, 5.0)
        glEnd()

        horzborder()
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y-0.01, 5.0)
        glTexCoord2f(xsize/0.05 * 2, 0.0)
        glVertex3f(x+xsize, y-0.01, 5.0)
        glTexCoord2f(xsize/0.05 * 2, 1.0)
        glVertex3f(x+xsize, y, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y, 5.0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y+ysize, 5.0)
        glTexCoord2f(xsize/0.05 * 2, 0.0)
        glVertex3f(x+xsize, y+ysize, 5.0)
        glTexCoord2f(xsize/0.05 * 2, 1.0)
        glVertex3f(x+xsize, y+ysize+0.01, 5.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y+ysize+0.01, 5.0)
        glEnd()

        vertborder()
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x-0.01, y, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x, y, 5.0)
        glTexCoord2f(1.0, ysize/0.05 * 2)
        glVertex3f(x, y+ysize, 5.0)
        glTexCoord2f(0.0, ysize/0.05 * 2)
        glVertex3f(x-0.01, y+ysize, 5.0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x+xsize, y, 5.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x+xsize+0.01, y, 5.0)
        glTexCoord2f(1.0, ysize/0.05 * 2)
        glVertex3f(x+xsize+0.01, y+ysize, 5.0)
        glTexCoord2f(0.0, ysize/0.05 * 2)
        glVertex3f(x+xsize, y+ysize, 5.0)
        glEnd()

        glPushMatrix()
        glTranslate(0.0, 0.0, 6.0)
        for s in self.spec:
            if s[0][:3] == '***':
                bits = s[0][3:].split('.')
                t = texture.Text(str(getattr(self.char, bits[0]).get(bits[1])), drawfont, s[3] * screen.height)
            elif s[0][:2] == '**':
                t = texture.Text(str(getattr(self.char, s[0][2:])), drawfont, s[3] * screen.height)
            elif s[0][:1] == '@':
                t = texture.Text(s[0][1:], drawfont, s[3] * screen.height)
                hsize = t.horizsize(s[3])
                buttonbg()
                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0)
                glVertex3f(x+s[1]-0.005, y+s[2], -0.01)
                glTexCoord2f(1.0, 0.0)
                glVertex3f(x+s[1]+hsize+0.005, y+s[2], -0.01)
                glTexCoord2f(1.0, 1.0)
                glVertex3f(x+s[1]+hsize+0.005, y+s[2]+s[3], -0.01)
                glTexCoord2f(0.0, 1.0)
                glVertex3f(x+s[1]-0.005, y+s[2]+s[3], -0.01)
                glEnd()
            elif s[0][:1] == '$':
                t = None
                image = media.loadtexture(s[0][1:])
                image()
                width = s[3] * image.size[0]/image.size[1]
                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0)
                glVertex2f(x+s[1], y+s[2])
                glTexCoord2f(1.0, 0.0)
                glVertex2f(x+s[1]+width, y+s[2])
                glTexCoord2f(1.0, 1.0)
                glVertex2f(x+s[1]+width, y+s[2]+s[3])
                glTexCoord2f(0.0, 1.0)
                glVertex2f(x+s[1], y+s[2]+s[3])
                glEnd()
            else:
                t = texture.Text(s[0], drawfont, s[3] * screen.height)
            if t:
                t.render((x+s[1], y+s[2]), s[3])
        glPopMatrix()
