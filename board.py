from OpenGL.GL import *
from OpenGL.GLU import *
import math
from array import array
import texture
import pprint

class character:
    def __init__ (self, texture):
        self.texture = texture
    def __call__ (self):
        self.texture()

class tile:
    def __init__ (self, texture):
        self.texture = texture
        self.contents = None
        self.passable = True
    def draw (self, pos, size):
        self.texture()
        x, y = pos
        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x, y)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x, y+size)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x+size, y+size)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x+size, y)
        glEnd()
        if self.contents:
            self.contents()
            glBegin(GL_QUADS)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x, y, 1.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x, y+size, 1.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x+size, y+size, 1.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x+size, y, 1.0)
            glEnd()


class board:
    def __init__ (self):
        self.pos = [0, 0]
        self.selected = None
        self.selectedtexture = texture.Texture("Border.png")
        self.board = array(30, 30)
        self.size = self.board.size
        self.enemy = texture.Texture("Enemy.png")
        grass = texture.Texture("Grass.png")
        ocean = texture.Texture("Ocean.png")
        for x in xrange(self.size[0]):
            for y in xrange (self.size[1]):
                if (x+y) % 2 == 0:
                    self.board[x, y] = tile(grass)
                else:
                    self.board[x, y] = tile(ocean)
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
        for x, i in zip(range(self.size[0]), [z/self.screensize for z in xrange(self.size[0])]):
            for y, j in zip(range(self.size[1]), [z/self.screensize for z in xrange(self.size[1])]):
                self.board[x, y].draw((i, j), tilesize)
        glTranslate(0.0, 0.0, 0.1)
        if self.selected:
            x = self.selected[0]/self.screensize
            y = self.selected[1]/self.screensize
            self.selectedtexture()
            glBegin(GL_QUADS)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x, y, 4.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x, y+tilesize, 4.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x+tilesize, y+tilesize, 4.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x+tilesize, y, 4.0)
            glEnd()            
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
    def select (self, pos):
        self.selected = (int(math.floor(self.screensize * (pos[0] + self.pos[0]))),
                         int(math.floor(self.screensize * (pos[1] + self.pos[1]))))
        self.board.reference(self.selected).contents = character(self.enemy)
