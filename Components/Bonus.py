from Components.Image import *

class Bonus:

    speed = 2

    def __init__(self):
        self.image = SpriteSheet("Ressources/Sprites/pastille.png", 3, 2)
        self.image.setArea(0)
        self.area = self.image.getArea()
        self.Surface = self.image.Surface
        self.Rect = self.getRect()

        self.animationDelay = 30 #ms
        self.animationTimer = pygame.time.get_ticks()

    def setPosition(self, x, y):
        self.image.setPosition(x, y)
        self.Rect = self.getRect()

    def getRect(self):
        return self.image.Rect

    def linearWalk(self):
        self.setPosition(0, Bonus.speed)

    # Initialise la valeur area, la zone à afficher dans une spritesheet
    def setArea(self):
        # Si le temps depuis le dernier appel + le delay sont toujours supérieur,
        #   on attend que le temps passe
        if self.animationTimer + self.animationDelay < pygame.time.get_ticks():
            self.image.currentFrame += 1
            if self.image.currentFrame >= self.image.number:
                #Si on depasse le nombre d'images dans la sprite, on revient à la premiere
                self.image.currentFrame = 0
            self.image.setArea(self.image.currentFrame)
            self.area = self.image.getArea()
            self.animationTimer = pygame.time.get_ticks()
