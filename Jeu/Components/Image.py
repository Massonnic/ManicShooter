import pygame

# Class pour les images simples
class Image:

    def __init__(self, src, alpha = 0):
        if alpha:
            self.Surface = pygame.image.load(src).convert_alpha()
        else:
            self.Surface = pygame.image.load(src).convert()

        self.Rect = self.Surface.get_rect()

    def setPosition(self, x, y):
        self.Rect = self.Rect.move(x, y)

# Classe pour créer soit même les Surfaces et les remplir d'une couleur
class Surface(Image):

    def __init__(self, dimension):
        self.Surface = pygame.Surface(dimension)
        self.Rect = self.Surface.get_rect()

    def fill(self, color):
        self.Rect = self.Surface.fill(color)

# Class pour les images composées (sprite pour animation)
class SpriteSheet(Image):

    def __init__(self, src, row, column, miss = 0):
        # Attributs de l'image composée (spritesheet)
        # miss permettant de gerer le nombre d'images manquantes sur la dernière ligne
        self.column = column
        self.row = row
        self.miss = miss
        self.currentFrame = 0

        self.image = Image(src, 1)
        self.Surface = self.image.Surface
        self.number = (self.column * self.row) - miss
        self.height = int(self.Surface.get_height() / self.row)
        self.width = int(self.Surface.get_width() / self.column)
        self.Rect = pygame.Rect(0, 0, self.width, self.height)

        self.createList()

    # Méthode de creation du tableau de rectangles des frames de l'image du joueur
    def createList(self):
        self.table = []
        for i in range(self.number):
            left, top = i % self.column * self.width, i // self.column * self.height
            self.table.append(pygame.Rect(left, top, self.width, self.height))

    def getSprite(self, index):
        return self.table[index]

    def setArea(self, index):
        self.area = self.getSprite(index)

    def getArea(self):
        return self.area
