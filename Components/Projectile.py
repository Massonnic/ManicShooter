import pygame
from Components.Image import *
pygame.mixer.init()

class Projectile:

    playSound = True

    def __init__(self, id, song):

        self.image = Projectile.getImageById(id)
        self.image.setArea(0)
        self.area = self.image.getArea()
        self.Surface = self.image.Surface
        self.Rect = self.getRect()
        self.width = self.image.width
        self.height = self.image.height

        self.animationDelay = 120 #ms
        self.animationTimer = pygame.time.get_ticks()

        self.song = song
        self.sound = pygame.mixer.Sound(self.song)

        if Projectile.playSound:
            self.sound.play().set_volume(0.5)

    def setPosition(self, x, y):
        self.image.setPosition(x, y)
        self.Rect = self.image.Rect

    def getRect(self):
        return self.image.Rect

    def changeSong(self, song):
        self.song = song

    def isInWindow(self, hostileTir = False):
        if not hostileTir:
            if self.Rect.top > 0:
                return True
        else:
            if self.Rect.top < 700:
                return True
        return False

    def getImageById(id):
        if id == 1:
            image = SpriteSheet("Ressources/Sprites/feu.png", 1, 1)
        elif id == 2:
            image = SpriteSheet("Ressources/Sprites/flamme.png", 1, 1)
        elif id == 3:
            image = SpriteSheet("Ressources/Sprites/tirVert.png", 2, 3)
        elif id == 4:
            image = SpriteSheet("Ressources/Sprites/tirBleu.png", 2, 3)
        elif id == 5:
            image = SpriteSheet("Ressources/Sprites/boule.png", 2, 2)
        elif id == 6:
            image = SpriteSheet("Ressources/Sprites/boule2.png", 2, 3, 1)
        elif id == 7:
            image = SpriteSheet("Ressources/Sprites/boulet.png", 1, 1)

        return image

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
