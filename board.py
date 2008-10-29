from OpenGL.GL import *
from OpenGL.GLU import *
import math
from array import array
import texture
#import pprint
import shelve
from media import loadtexture
from chars import character

initialized = False

def addadjacent(coord, dist, queue):
    queue.insert(len(queue), (dist+1, (coord[0],   coord[1]+1)))
    queue.insert(len(queue), (dist+1, (coord[0],   coord[1]-1)))
    queue.insert(len(queue), (dist+1, (coord[0]+1, coord[1])))
    queue.insert(len(queue), (dist+1, (coord[0]-1, coord[1])))

def withinbounds((x,y), (xsize, ysize)):
    return 0 <= x < xsize and 0 <= y < ysize

def drawsquare((x,y), xsize, ysize, texture, depth = 0, color = (1.0, 1.0, 1.0, 1.0), tilt = 0.0):
    if texture:
        texture()
    else:
        glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glColor(color)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, depth + tilt)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y+ysize, depth)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x+xsize, y+ysize, depth)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x+xsize, y, depth + tilt)
    glEnd()

def deserialize(obj):
    if not obj:
        return None
    if obj[0] == 'character':
        t = loadtexture(obj[1].split('/')[-1])
        c = character(t, obj[2])
        c.stats = obj[3]
        return c
    if obj[0] == 'tile':
        t = loadtexture(obj[1])
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
        drawsquare(pos, size, size, self.texture)
        if showpassable:
            if self.passable:
                drawsquare(pos, size, size, None, 1.0, (0.1, 0.3, 1.0, 0.3))
            else:
                drawsquare(pos, size, size, None, 1.0, (1.0, 0.1, 0.3, 0.3))
    def drawcontents(self, pos, size):
        if self.contents:
            pos = list(pos)
            pos[1] -= 1.0/screensize
            if self.contents.stats['ct'] == 1.0:
                drawsquare(pos, size, size*2, self.contents, 2.0, (1.0,1.0,1.0,1.0), 0.5)
            else:
                drawsquare(pos, size, size*2, self.contents, 2.0, (1.0,1.0,1.0,0.5), 0.5)
    def togglepassable(self):
        self.passable = not self.passable
    def mark(self, pos, size, color = (0.0, 0.0, 1.0, 0.3)):
        drawsquare(pos, size, size, None, 2.0, color)
    def serialize(self):
        if self.contents:
            return ['tile', self.texture.name, self.contents.serialize(), self.passable]
        else:
            return ['tile', self.texture.name, None, self.passable]

def init (s = (20, 20), loadfrom = None):
    global pos, selected, selectedtexture, board, size, showpassable, moving, attacking, screensize, initialized
    initialized = True
    pos = [0, 0]
    selected = None
    selectedtexture = loadtexture("Border.png")
    board = array(*s)
    size = board.size
    clearmarks()
    showpassable = False
    moving = False
    attacking = False
    screensize = 10.0
    if loadfrom:
        load(loadfrom)
        return
    grass = loadtexture("grass.png")
    ocean = loadtexture("water.png")
    for x in xrange(size[0]):
        for y in xrange (size[1]):
            if x % 10 == 0 or y % 10 == 0:
                board[x, y] = tile(ocean)
            else:
                board[x, y] = tile(grass)
    enemytexture = loadtexture("Enemy.png")
    herotexture = loadtexture("Hero.png")
    board[0,0].contents = character(herotexture, "Hero 1")
    board[3,0].contents = character(herotexture, "Hero 2")
    board[6,0].contents = character(herotexture, "Hero 3")
    board[9,0].contents = character(herotexture, "Hero 4")
    for x in xrange(size[0]):
        board[x,5].passable = False
    board[5,5].passable = True
    for x in xrange(size[0]):
        board[x, 7].contents = character(enemytexture, "Enemy %i" % (x+1))
def load(mapname):
    global board
    print "load", mapname
    map = shelve.open(mapname)
#   pprint.pprint(map['board'])
    board = array(*map['boardsize'])
    board.array = [deserialize(x) for x in map['board']]
def save(mapname):
    map = shelve.open(mapname)
    map["gamename"] = "default"
    map["boardsize"] = board.size
    b = [tile.serialize() for tile in board.array]        
    map["board"] = b
    map.close()
    print "save", mapname
def movemap (delta):
    global pos
    pos[0] += delta[0]
    pos[0] = max(0, min(size[0]/screensize - 4.0/3.0, pos[0]))
    pos[1] += delta[1]
    pos[1] = max(0, min(size[1]/screensize - 1, pos[1]))
def draw ():
    global screensize
    tilesize = 1.0/screensize
    glPushMatrix()
    glTranslatef(-pos[0], -pos[1], 0.0)
    for x, i in enumerate([z/screensize for z in xrange(size[0])]):
        for y, j in enumerate([z/screensize for z in xrange(size[1])]):
            board[x, y].draw((i, j), tilesize, showpassable)
    glTranslate(0.0, 0.0, 0.1)
    for p in marklist:
        if attacking:
            board.reference(p).mark(tuple(i/screensize for i in p), tilesize, (1.0, 0.0, 0.0, 0.3))
        else:
            board.reference(p).mark(tuple(i/screensize for i in p), tilesize)
    for x, i in enumerate([z/screensize for z in xrange(size[0])]):
        for y, j in enumerate([z/screensize for z in xrange(size[1])]):
            board[x, y].drawcontents((i, j), tilesize)
    if selected:
        x = selected[0]/screensize
        y = selected[1]/screensize
        drawsquare((x,y), tilesize, tilesize, selectedtexture, 4.0)
    #drawgrid()
    glPopMatrix()
def drawgrid():
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_LINES)
    glColor4f(0.0, 0.0, 0.0, 1.0)
    for i in [x/screensize for x in xrange(int(size[0]))]:
        glVertex3f(i, 0.0, 4.5)
        glVertex3f(i, size[1]/screensize, 4.5)
    for i in [x/screensize for x in xrange(int(size[1]))]:
        glVertex3f(0.0, i, 4.5)
        glVertex3f(size[0]/screensize, i, 4.5)
    glEnd()
def screentoworld(p):
    global pos
    return (int(math.floor(screensize * (p[0] + pos[0]))),
            int(math.floor(screensize * (p[1] + pos[1]))))
def select (p):
    global moving, attacking, selected
    if moving:
        if move(screentoworld(p)):
            moving = False
    elif attacking:
        if attack(screentoworld(p)):
            attacking = False
    else:
        selected = screentoworld(p)
def move (moveto):
    global selected
    if selected and moveto in marklist:
        setcontents(moveto, getcontents(selected))
        setcontents(selected, None)
        selected = moveto
        getcontents(selected).stats['ct'] = 0.0
        clearmarks()
        return True
    return False
def markmove():
    global marklist
    if not (getselected() and getselected().contents):
        return False
    range = getselected().contents.stats['move']
    clearmarks()
    queue = []
    addadjacent(selected, 0, queue)
    while len(queue) > 0:
        dist, current_square = queue.pop(0)
        if dist <= range and withinbounds(current_square, size) and ispassable(current_square)\
                and not getcontents(current_square) and current_square not in marklist:
            marklist.insert(len(queue), current_square)
            addadjacent(current_square, dist, queue)
    if marklist == []:
        return False
    return True
def attack(attackto):
    global selected
    if selected and attackto in marklist and getcontents(attackto) != None:
        attacker = getcontents(selected)
        defender = getcontents(attackto)
        damage = math.floor(attacker.stats['pa'] + attacker.stats['level'] - defender.stats['level'] * 
                            defender.stats['pd'] / defender.stats['pa'])
        if damage >= defender.stats['hp']:
            #defender is dead
            attackto.contents = None
        else:
            defender.stats['hp'] = int(defender.stats['hp'] - damage)
        clearmarks()
        return True
    return False
def markattack():
    global marklist, selected
    if not (getselected() and getselected().contents):
        return False
    adjacent = []
    addadjacent(selected, 0, adjacent)
    adjacent = [x[1] for x in adjacent]
    for a in adjacent:
        marklist.insert(0, a)
    if marklist == []:
        return False
    return True
def ispassable(pos):
    return board.reference(pos).passable
def getcontents(pos):
    return board.reference(pos).contents
def setcontents(pos, contents):
    board.reference(pos).contents = contents
def getselected():
    if selected:
        return board.reference(selected)
    else:
        return None
def getselectedcontents():
    s = getselected()
    if s:
        return s.contents
    else:
        return None
def clearmarks():
    global marklist
    marklist = []
def toggleshowpassable():
    global showpassable
    showpassable = not showpassable
def startmove():
    global moving, attacking
    attacking = False
    if moving:
        moving = False
        clearmarks()
    elif markmove():
        moving = True
def startattack():
    global attacking, moving
    moving = False
    if attacking:
        attacking = False
        clearmarks()
    elif markattack():
        attacking = True
def allofside(side):
    return [y for y in allchars() if y.side == side]
def allchars():
    return [x.contents for x in board.array if x.contents]
def advtime():
    next = None
    timetonext = 0
    for c in allchars():
        if next == None:
            next = c
            timetonext = (1.0 - c.stats['ct'])/c.stats['speed']
        else:
            timetoturn = (1.0 - c.stats['ct'])/c.stats['speed']
            if timetoturn < timetonext:
                next = c
                timetonext = timetoturn
    for c in allchars():
        c.stats['ct'] += c.stats['speed'] * timetonext
    return next
