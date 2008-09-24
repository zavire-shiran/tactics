

class character:
    def __init__ (self, texture, name):
        self.texture = texture
        self.name = name
        self.stats = {}
        self.stats['hp'] = 50
        self.stats['tp'] = 30
        self.stats['pa'] = 25
        self.stats['pd'] = 10
        self.stats['sp'] = 5
        self.stats['sr'] = 5
        self.stats['speed'] = 100
        self.stats['move'] = 3
        if name[0] == 'H':
            self.stats['side'] = 0
        elif name[0] == 'E':
            self.stats['side'] = 1
    def __call__ (self):
        self.texture()
    def serialize(self):
        return ['character', self.texture.name, self.name, self.stats]
