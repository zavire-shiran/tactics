import os
import texture

textures = {}

def act(i):
    return i.split('/', 2)[1], x[0] + '/' + i

def dircontents(dir):
    ret = []
    walker = os.walk(dir)
    l = len(dir)+1
    for x in walker:
        ret += [(i, x[0] + '/' + i) for i in x[2]]
    return ret

def loadtexture(name):
    if name not in textures:
        dircon = dict(dircontents('terrain') + dircontents('data') + dircontents('entities'))
        try:
            textures[name] = texture.Texture(dircon[name])
        except KeyError:
            textures[name] = texture.Texture(name)
    return textures[name]
