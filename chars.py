

class character:
    def __init__ (self, texture, name):
        self.texture = texture
        self.name = name
        self.hp = 50
        self.tp = 30
        self.pa = 25
        self.pd = 10
        self.sp = 5
        self.sr = 5
        self.speed = 100
        self.move = 3
        self.moved = False
        if name[0] == 'H':
            self.side = 0
        elif name[0] == 'E':
            self.side = 1
    def __call__ (self):
        self.texture()
    def serialize(self):
        return ['character', self.texture.name, self.hp, self.tp, self.pa, self.pd, self.sp, self.sr, self.speed, self.move]

