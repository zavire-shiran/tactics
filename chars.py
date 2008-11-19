import media

defaultstats = {'hp': 50, 'maxhp': 50, 'tp': 30, 'maxtp': 30, 'pa': 25, 'pd': 10, 'sp': 5, 'sr': 5, 'level': 1,
                'speed': 100, 'move': 3, 'side': 0, 'ct': 0, 'level': 10, 'xp': 0, 'ct': 0.0}

class animset:
    def __init__(self, file):
        self.name = file
        self.idle = open('animsets/'+file).readline().strip()
         
class character:
    def __init__ (self, animset, name):
        self.setanimset(animset)
        self.name = name
        self.stats = {}
        self.moved = False
        self.checkstats()
    def setanimset(self, set):
        self.animset = animset(set)
        self.texture = media.loadtexture(self.animset.idle)
    def checkstats(self):
        for k,v in defaultstats.iteritems():
            if k not in self.stats:
                self.stats[k] = v
        for k in self.stats.keys():
            if k not in defaultstats:
                del self.stats[k]
    def __call__ (self):
        self.texture()
    def serialize(self):
        return ['character', self.animset.name, self.name, self.stats]
