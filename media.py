import os
import texture

textures = {}

def dircontents(dir):
    return [(i, dir+'/'+i) for i in os.listdir(dir)]

def loadtexture(name):
    if name not in textures:
        dircon = dict(dircontents('terrain') + dircontents('data') + dircontents('entities'))
        textures[name] = texture.Texture(dircon[name])
    return textures[name]
