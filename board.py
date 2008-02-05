from OpenGL.GL import *
from OpenGL.GLU import *
import text
import math
from array import array

class board:
    def __init__ (self, texture):
        self.texture = texture
        self.pos = [0, 0]
        self.selected = None
        self.board = array(30, 30)
        self.size = self.board.size
        self.screensize = 10.0
    def move (self, delta):
        self.pos[0] += delta[0]
        self.pos[0] = min(self.size[0]/self.screensize - 1, max(0, self.pos[0]))
        self.pos[1] += delta[1]
        self.pos[1] = min(self.size[1]/self.screensize - 1, max(0, self.pos[1]))
    def draw (self):
        tilesize = 1.0/self.screensize
        glPushMatrix()
        glTranslatef(-self.pos[0], -self.pos[1], 0.0)
        text.render("Hello")
        for i in [x/self.screensize for x in xrange(int(self.size[0]))]:
            for j in [x/self.screensize for x in xrange(int(self.size[1]))]:
                self.texture()
                glBegin(GL_QUADS)
                glColor4f(1.0, 1.0, 1.0, 1.0)
                glTexCoord2f(0.0, 0.0)
                glVertex2f(i, j)
                glTexCoord2f(0.0, 1.0)
                glVertex2f(i, j+tilesize)
                glTexCoord2f(1.0, 1.0)
                glVertex2f(i+tilesize, j+tilesize)
                glTexCoord2f(1.0, 0.0)
                glVertex2f(i+tilesize, j)
                glEnd()
        glTranslate(0.0, 0.0, 0.1)
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_LINES)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        for i in [x/self.screensize for x in xrange(int(self.size[0]))]:
            glVertex2f(i, 0.0)
            glVertex2f(i, self.size[1]/self.screensize)
        for i in [x/self.screensize for x in xrange(int(self.size[1]))]:
            glVertex2f(0.0, i)
            glVertex2f(self.size[0]/self.screensize, i)
        glEnd()
        glPopMatrix()
    def select(self, pos):
        self.selected = (int(math.floor(self.screensize * (pos[0] + self.pos[0]))),
                         int(math.floor(self.screensize * (pos[1] + self.pos[1]))))
        print self.selected
