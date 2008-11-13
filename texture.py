from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import math
import media

class Texture:
    def __init__(self, f):
        self.name = f
        surf = pygame.image.load(f)           
        #surf = sizeof2ify(surf)
        width, height = surf.get_size()
        glEnable(GL_TEXTURE_2D)
        self.textnum = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textnum)

        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE,
                          pygame.image.tostring(surf, "RGBA"))

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    def __call__(self):
        self.bind()

    def __del__(self):
        glDeleteTextures([self.textnum])

    def bind(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textnum)

class Text:
    def __init__(self, text, font, size = 20):
        font = pygame.font.Font(font, int(size + 0.5))
        surf = font.render(text, True, (255, 255, 255))
        origwidth, origheight = surf.get_size()
        surf = sizeof2ify(surf)
        width, height = surf.get_size()
        self.origbounds = origwidth, origheight
        self.bounds = (float(origwidth) / width, float(origheight) / height)

        glEnable(GL_TEXTURE_2D)
        self.textnum = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textnum)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE,
                          pygame.image.tostring(surf, "RGBA"))

    def __del__(self):
        glDeleteTextures([self.textnum])

    def __call__(self):
        self.bind()

    def horizsize(self, drawheight):
        return (drawheight / self.origbounds[1]) * self.origbounds[0]

    def bind (self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textnum)

    def render(self, pos, drawheight):
        self.bind()
        width, height = self.bounds
        origwidth, origheight = self.origbounds
        scale = drawheight / origheight
        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(pos[0], pos[1])
        glTexCoord2f(0.0, height)
        glVertex2f(pos[0], pos[1] + drawheight)
        glTexCoord2f(width, height)
        glVertex2f(pos[0] + origwidth * scale, pos[1] + drawheight)
        glTexCoord2f(width, 0.0)
        glVertex2f(pos[0] + origwidth * scale, pos[1])
        glEnd()

def horizsize(text, font, drawheight):
    font = pygame.font.Font(font, 18)
    rsize = font.size(text)
    return (float(drawheight) / rsize[1]) * rsize[0]

def sizeof2ify(surf):
    ret = pygame.Surface([int(nextpowerof2(x)) for x in surf.get_size()], 0, surf)
    ret.blit(surf, (0, 0))
    return ret

def nextpowerof2(num):
    return 2 ** math.ceil(math.log(num, 2))

animations = []

class Animation:
    def __init__(self, f):
        global animations
        f = file(f)
        timing = [x.split() for x in f.readlines()]
        self.timing = [(media.loadtexture(x), float(y)) for x, y in timing]
        self.frame = 0
        self.time = 0.0
        animations.append(self)
    def tick(self, dt):
        self.time += dt
        while self.time >= self.timing[self.frame][1]:
            self.time -= self.timing[self.frame][1]
            self.frame += 1
            if self.frame >= len(self.timing):
                self.frame = 0
    def bind(self):
        self.timing[self.frame][0].bind()
    def __call__(self):
        self.bind()
