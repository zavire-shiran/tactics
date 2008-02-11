from OpenGL.GL import *
from OpenGL.GLU import *
import math
from array import array
import texture
import pprint

class character:
    def __init__ (self, texture, name):
        self.texture = texture
        self.name = name
    def __str__ (self):
        return self.name
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
        grass = texture.Texture("Grass.png")
        ocean = texture.Texture("Ocean.png")
        for x in xrange(self.size[0]):
            for y in xrange (self.size[1]):
                if x % 10 == 0 or y % 10 == 0:
                    self.board[x, y] = tile(ocean)
                else:
                    self.board[x, y] = tile(grass)
        self.screensize = 15.0

        enemytexture = texture.Texture("Enemy.png")
        herotexture = texture.Texture("Hero.png")
        self.board[0,0].contents = character(herotexture, "Hero 1")
        self.board[5,0].contents = character(herotexture, "Hero 2")
        self.board[9,0].contents = character(herotexture, "Hero 3")
        for x in xrange(self.size[0]):
            self.board[x, 7].contents = character(enemytexture, "Enemy %i" % (x+1))
    def movemap (self, delta):
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
            glVertex3f(i, 0.0, 4.9)
            glVertex3f(i, self.size[1]/self.screensize, 4.5)
        for i in [x/self.screensize for x in xrange(int(self.size[1]))]:
            glVertex3f(0.0, i, 4.9)
            glVertex3f(self.size[0]/self.screensize, i, 4.5)
        glEnd()
        glPopMatrix()
    def screentoworld(self, pos):
        return (int(math.floor(self.screensize * (pos[0] + self.pos[0]))),
                int(math.floor(self.screensize * (pos[1] + self.pos[1]))))
    def select (self, pos):
        newselection = self.screentoworld(pos)
        if self.selected and \
           self.getcontents(self.selected) and \
           not self.getcontents(newselection):
            self.setcontents(newselection, self.getcontents(self.selected))
            self.setcontents(self.selected, None)
        self.selected = newselection
    def getcontents(self, pos):
        return self.board.reference(pos).contents
    def setcontents(self, pos, contents):
        self.board.reference(pos).contents = contents
    def getselected(self):
        if self.selected:
            return self.board.reference(self.selected)
        else:
            return None
