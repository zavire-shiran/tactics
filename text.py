from pygame import font

Font = None

def render(text):
    global Font
    if Font == None:
        Font = font.Font(None, 14)
    Font.render(text, True, (0, 0, 0))
