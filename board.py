from OpenGL.GL import *
from OpenGL.GLU import *
import math
from array import array
import texture
#import pprint
import shelve

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
        self.moved = False
        if name[0] == 'H':
            self.side = 0
        elif name[0] == 'E':
            self.side = 1
    def __str__ (self):
        return '\n'.join([str(i) for i in
                          [self.name, 
                           "Move: %s" % self.move, 
                           "ST: %s" % self.str, 
                           "DX: %s" % self.dex, 
                           "IQ: %s" % self.iq, 
                           "HT: %s" % self.ht,
                           "Moved: %s" % self.moved]])
    def __call__ (self):
        self.texture()
    def serialize(self):
        return ['character', self.texture.name, self.name, self.move, self.str, self.dex, self.iq, self.ht]

textures = {}

def deserialize(obj):
    global textures
    if not obj:
        return None
    if obj[0] == 'character':
        if obj[1] not in textures:
            textures[obj[1]] = texture.Texture(obj[1])
        t = textures[obj[1]]
        c = character(t, obj[2])
        c.move = obj[3]
        c.str = obj[4]
        c.dex = obj[5]
        c.iq = obj[6]
        c.ht = obj[7]
        return c
    if obj[0] == 'tile':
        if obj[1] not in textures:
            textures[obj[1]] = texture.Texture(obj[1])
        t = textures[obj[1]]
        tl = tile(t)
        tl.contents = deserialize(obj[2])
        tl.passable = obj[3]
        return tl

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
    def togglepassable(self):
        self.passable = not self.passable
    def mark(self, pos, size):
        drawsquare(pos, size, None, 3.0, (0.0, 0.0, 1.0, 0.3))
    def serialize(self):
        if self.contents:
            return ['tile', self.texture.name, self.contents.serialize(), self.passable]
        else:
            return ['tile', self.texture.name, None, self.passable]

class board:
    def __init__ (self):
        self.pos = [0, 0]
        self.selected = None
        self.selectedtexture = texture.Texture("Border.png")
        self.board = array(30, 30)
        self.size = self.board.size
        self.clearmarks()
        self.showpassable = False
        self.moving = False
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
    def load(self, mapname):
        print "load", mapname
        map = shelve.open(mapname)
#       pprint.pprint(map['board'])
        self.board = array(*map['boardsize'])
        self.board.array = [deserialize(x) for x in map['board']]
    def save(self, mapname):
        map = shelve.open(mapname)
        map["gamename"] = "default"
        map["boardsize"] = self.board.size
        board = [tile.serialize() for tile in self.board.array]        
        map["board"] = board
        map.close()
        print "save", mapname
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
        if self.moving:
            if self.move(self.screentoworld(pos)):
                self.moving = False
        else:
            self.selected = self.screentoworld(pos)
    def move (self, moveto):
        if self.selected and \
           moveto in self.marklist:
            self.setcontents(moveto, self.getcontents(self.selected))
            self.setcontents(self.selected, None)
            self.selected = moveto
            self.clearmarks()
            return True
        return False
    def markmove(self):
        if not (self.getselected() and self.getselected().contents):
            return False
        range = self.getselected().contents.move
        self.clearmarks()
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
    def startmove(self):
        if self.moving:
            self.moving = False
            self.clearmarks()
        elif self.markmove():
            self.moving = True
    def allofside(self, side):
        return filter(lambda x: x.side == side, filter(None, [x.contents for x in self.board.array]))
