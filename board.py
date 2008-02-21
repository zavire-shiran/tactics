from OpenGL.GL import *
from OpenGL.GLU import *
import math
from array import array
import texture
import pprint

def addadjacent(coord, dist, queue):
    queue.insert(len(queue), (dist+1, (coord[0],   coord[1]+1)))
    queue.insert(len(queue), (dist+1, (coord[0],   coord[1]-1)))
    queue.insert(len(queue), (dist+1, (coord[0]+1, coord[1])))
    queue.insert(len(queue), (dist+1, (coord[0]-1, coord[1])))

def withinbounds((x,y), (xsize, ysize)):
    return 0 <= x < xsize and 0 <= y < ysize

def drawsquare((x,y), size, texture, depth = 0, color = (1.0, 1.0, 1.0, 1.0)):
    if texture:
        texture()
    else:
        glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glColor(color)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, depth)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y+size, depth)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x+size, y+size, depth)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x+size, y, depth)
    glEnd()

class character:
    def __init__ (self, texture, name):
        self.texture = texture
        self.name = name
        self.move = 5
        self.str = 10
        self.dex = 10
        self.iq = 10
        self.ht = 10
    def __str__ (self):
        return '\n'.join([str(i) for i in [self.name, 
                                           "Move: %s" % self.move, 
                                           "ST: %s" % self.str, 
                                           "DX: %s" % self.dex, 
                                           "IQ: %s" % self.iq, 
                                           "HT: %s" % self.ht]])
    def __call__ (self):
        self.texture()

class tile:
    def __init__ (self, texture):
        self.texture = texture
        self.contents = None
        self.passable = True
    def draw (self, pos, size, showpassable = False):
        self.texture()
        x, y = pos
        drawsquare(pos, size, self.texture)
        if showpassable:
            if self.passable:
                drawsquare(pos, size, None, 1.0, (0.1, 0.3, 1.0, 0.3))
            else:
                drawsquare(pos, size, None, 1.0, (1.0, 0.1, 0.3, 0.3))
        if self.contents:
            drawsquare(pos, size, self.contents, 2.0)

    def mark(self, pos, size):
        drawsquare(pos, size, None, 3.0, (0.0, 0.0, 1.0, 0.3))

class board:
    def __init__ (self):
        self.pos = [0, 0]
        self.selected = None
        self.selectedtexture = texture.Texture("Border.png")
        self.board = array(15, 15)
        self.size = self.board.size
        self.clearmarks()
        self.showpassable = False
        grass = texture.Texture("Grass.png")
        ocean = texture.Texture("Ocean.png")
        for x in xrange(self.size[0]):
            for y in xrange (self.size[1]):
                if x % 10 == 0 or y % 10 == 0:
                    self.board[x, y] = tile(ocean)
                else:
                    self.board[x, y] = tile(grass)
        self.screensize = 10.0
        enemytexture = texture.Texture("Enemy.png")
        herotexture = texture.Texture("Hero.png")
        self.board[0,0].contents = character(herotexture, "Hero 1")
        self.board[3,0].contents = character(herotexture, "Hero 2")
        self.board[6,0].contents = character(herotexture, "Hero 3")
        self.board[9,0].contents = character(herotexture, "Hero 4")
        for x in xrange(self.size[0]):
            self.board[x,5].passable = False
        self.board[5,5].passable = True
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
        for x, i in enumerate([z/self.screensize for z in xrange(self.size[0])]):
            for y, j in enumerate([z/self.screensize for z in xrange(self.size[1])]):
                self.board[x, y].draw((i, j), tilesize, self.showpassable)
        glTranslate(0.0, 0.0, 0.1)
        for p in self.marklist:
            self.board.reference(p).mark(tuple(i/self.screensize for i in p), tilesize)
        if self.selected:
            x = self.selected[0]/self.screensize
            y = self.selected[1]/self.screensize
            drawsquare((x,y), tilesize, self.selectedtexture, 4.0)
        self.drawgrid()
        glPopMatrix()
    def drawgrid(self):
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
    def screentoworld(self, pos):
        return (int(math.floor(self.screensize * (pos[0] + self.pos[0]))),
                int(math.floor(self.screensize * (pos[1] + self.pos[1]))))
    def select (self, pos):
        self.selected = self.screentoworld(pos)
    def move (self, moveto):
        if self.selected and \
           moveto in self.marklist:
            self.setcontents(moveto, self.getcontents(self.selected))
            self.setcontents(self.selected, None)
            self.selected = moveto
            self.marklist = []
            return True
        return False
    def markmove(self):
        if not self.getselected():
            return False
        range = self.getselected().contents.move
        self.marklist = []
        queue = []
        addadjacent(self.selected, 0, queue)
        while len(queue) > 0:
            dist, current_square = queue.pop(0)
            if dist <= range and withinbounds(current_square, self.size) and self.ispassable(current_square)\
               and not self.getcontents(current_square) and current_square not in self.marklist:
                self.marklist.insert(len(queue), current_square)
                addadjacent(current_square, dist, queue)
        if self.marklist == []:
            return False
        return True
    def ispassable(self, pos):
        return self.board.reference(pos).passable
    def getcontents(self, pos):
        return self.board.reference(pos).contents
    def setcontents(self, pos, contents):
        self.board.reference(pos).contents = contents
    def getselected(self):
        if self.selected:
            return self.board.reference(self.selected)
        else:
            return None
    def clearmarks(self):
        self.marklist = []
    def toggleshowpassable(self):
        self.showpassable = not self.showpassable
