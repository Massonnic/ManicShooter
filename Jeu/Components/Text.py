import pygame

class Text:

    """Class définissant le texte:

    - la police (font)
    - sa surface (sprite)"""

    fontFamily = "Ressources/Fonts/bignoodletitling/big_noodle_titling.ttf"
    fontSize = 30
    fontColor = pygame.Color(0)

    def __init__(self, size = fontSize, font = fontFamily):
        self.Font = pygame.font.Font(font, size)

    def write(self, text, color = fontColor, antialias = 0, background = None):
        self.Surface = self.Font.render(text, antialias, color, background)

    def setPosition(self, x, y):
        self.Rect = self.Surface.get_rect().move(x, y)
