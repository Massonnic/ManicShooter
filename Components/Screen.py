import pygame

class Screen:

    """Class définissant la fenêtre:

    - sa dimension
    - le lien du fond"""

    size = (400, 700)

    def __init__(self):
        self.Surface = pygame.display.set_mode(Screen.size)
        self.height = self.Surface.get_height()
        self.width = self.Surface.get_width()

    # Méthode d'affiche sur l'ecran
    def blit(self, objet, y = 0, font = 0):
        if not y and not font:
            self.Surface.blit(objet.image.Surface, objet.image.Rect)
        elif not y and font:
            self.Surface.blit(objet.Surface, objet.Rect)
        else:
            self.Surface.blit(objet, y)

    # Identique à self.blit mais spécifique aux images composées
    def blit_area(self, objet):
        self.Surface.blit(objet.Surface, objet.Rect, objet.area)

    # Méthode pour "effacer" un element sous un autre élément
    def erase(self, source, dest):
        self.Surface.blit(source.Surface, dest.Rect, dest.Rect)

    def move(self, x, y):
        self.Rect = self.Rect.move(x, y)

    def scroll(self, x, y):
        self.Surface.scroll(x, y)
