s = None
b = None

def register(board, sidebar):
    global b, s
    b = board
    s = sidebar

def redosidebar():
    global b, s
    s.clearcontents()
    sel = b.getselected()
    if sel and sel.contents:
        first = True
        for line in str(sel.contents).split('\n'):
            if first:
                s.addtext(line, 0.06, 0.01)
                first = False
            else:
                s.addtext(line, 0.04, 0.005)
            s.addspacer(0.05)
            if b.moving:
                s.addbutton("Moving", 0.05, 0.01, lambda:b.startmove())
            else:
                s.addbutton("Not Moving", 0.05, 0.01, lambda:b.startmove())

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
            b.select((x,y))
            redosidebar()
    elif button == 3 and x < 1.0:
        b.movemap((x - 0.5, y - 0.5))
        redosidebar()
