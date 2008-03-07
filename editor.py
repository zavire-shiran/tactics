import os
import re

import texture

s = None
b = None
brush = None
imagenames = None
images = None

class functor:
    def __init__(self, function, *args):
        self.function = function
        self.args = args
    def __call__(self):
        self.function(*self.args)

def setbrush(image):
    global brush
    brush = image

def register(board, sidebar):
    global b, s, images, imagenames
    b = board
    s = sidebar
    imagenames = filter(lambda s: re.match('.*\.png', s), os.listdir('.'))
    images = map(texture.Texture, imagenames)
    redosidebar()

def redosidebar():
    global b, s, brush
    s.clearcontents()
    sel = b.getselected()
    for imagename, image in zip(imagenames, images):
        iname = imagename
        s.addbutton(imagename, 0.05, 0.01, functor(setbrush, image))

def keydown(key):
    if key == 'm':
        b.startmove()
        redosidebar()
    elif key == 'p':
        b.toggleshowpassable()

def mousedown(button, (x, y)):
    global b
    if button == 1:
        if x > 1.0:
            s.click(y)
            redosidebar()
        else:
            if brush:
                b.board.reference(b.screentoworld((x,y))).texture = brush
    elif button == 3 and x < 1.0:
        b.movemap((x - 0.5, y - 0.5))
        redosidebar()
