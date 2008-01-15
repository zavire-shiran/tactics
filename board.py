from OpenGL.GL import *
from OpenGL.GLU import *

class board:
    def __init__ (self, texture):
        self.texture = texture
    def draw (self, pos):
        glPushMatrix()
        glTranslatef(-pos[0], -pos[1], 0.0)
        self.texture()
        for i in [x/10.0 for x in range(10)]:
            for j in [x/10.0 for x in range(10)]:
                glBegin(GL_QUADS)
                glColor4f(1.0, 1.0, 1.0, 1.0)
                glTexCoord2f(0.0, 0.0)
                glVertex2f(i, j)
                glTexCoord2f(0.0, 1.0)
                glVertex2f(i, j+0.1)
                glTexCoord2f(1.0, 1.0)
                glVertex2f(i+0.1, j+0.1)
                glTexCoord2f(1.0, 0.0)
                glVertex2f(i+0.1, j)
                glEnd()
        glPopMatrix()
            
            
