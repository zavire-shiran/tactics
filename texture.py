from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import math

class Texture:
    def __init__(self, f):
        if isinstance(f, pygame.Surface):
            surf = f
        else:
            surf = pygame.image.load(f)           
        surf = sizeof2ify(surf)
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

    def bind(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textnum)

class Text:
    def __init__(self, text, font):
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

    def __call__(self):
        self.bind()

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

def sizeof2ify(surf):
    ret = pygame.Surface([int(nextpowerof2(x)) for x in surf.get_size()], 0, surf)
    ret.blit(surf, (0, 0))
    return ret

def nextpowerof2(num):
    return 2 ** math.ceil(math.log(num, 2))

