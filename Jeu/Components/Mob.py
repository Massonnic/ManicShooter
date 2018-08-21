from Components.Image import *
from Components.Projectile import *

class Mob:

    def __init__(self, objet):
        self.mob = objet
        self.image = Image(self.mob.get('image'), 1)
        self.Surface = self.image.Surface
        self.width = self.Surface.get_width()
        self.height = self.Surface.get_height()
        self.Rect = self.getRect()

        self.isdestroy = False
        self.isHostile = self.isHostile()

        self.patterns = []
        self.tirs = []
        self.tirSpeed = 5
        self.fireRate = 400
        self.lastShoot = 0
        self.song = 'Ressources/Songs/tir.wav'

        self.animationDelay = 60 #ms
        self.animationTimer = pygame.time.get_ticks()

    def events(self):
        self.execPatern()
        self.shootEvent()

    def setOrientation(self, angle):
        self.angle = angle
        self.image.Surface = pygame.transform.rotate(self.image.Surface, angle)

    def getRect(self):
        return self.image.Rect

    def setTimer(self, timer):
        self.timer = timer

    def getTimer(self):
        return pygame.time.get_ticks() - self.timer

    def getDepopTime(self):
        return self.mob.get('timeBeforeDepop')

    def isHostile(self):
        return self.mob.get('hostile')

    def setPosition(self, x, y):
        if self.isdestroy == 1:
            self.image.setPosition(x, (-y))
        else:
            self.image.setPosition(x, y)
        self.Rect = self.getRect()

    def shootEvent(self):
        for tir in self.tirs:
            tir.setArea()
            tir.setPosition(0, self.tirSpeed)
            if not tir.isInWindow(True):
                self.tirs.remove(tir)

    # Création du projectile en jeu et stockage de l'objet
    #   dans un tableau rassemblant tous les projectiles de l'ennemi
    def shoot(self):
        tir = Projectile(1, self.song)
        tir.setPosition(self.getRect().left + ((self.width - tir.width) /2), self.getRect().top + self.height + tir.height)
        self.tirs.append(tir)

    #Vérifie si l'entité est descendu jusqu'en bas
    def checkIfOut(self):
        if self.getRect()[1] > 700:
            return True
        return False

    #Recupère le comportement de l'ennemi
    def execPatern(self):
        for i in self.patterns:
            index = self.patterns.index(i)
            start = i['time']
            try:
                if self.getTimer() >= start and self.getTimer() < self.patterns[index+1]['time']:
                    id = i['id']
                    if id == 0:
                        self.mouvement0()
                    elif id == 1:
                        self.mouvement1()
                    elif id == 3:
                        self.mouvement3()
                    elif id == 4:
                        self.mouvement4()
                    elif id == 5:
                        self.mouvement5()
                    elif id == 6:
                        self.mouvement6()
                    elif id == 7:
                        self.mouvement7()
            except IndexError:
                if self.getTimer() >= start:
                    id = i['id']
                    if id == 0:
                        self.mouvement0()
                    elif id == 1:
                        self.mouvement1()
                    elif id == 3:
                        self.mouvement3()
                    elif id == 4:
                        self.mouvement4()
                    elif id == 5:
                        self.mouvement5()
                    elif id == 6:
                        self.mouvement6()
                    elif id == 7:
                        self.mouvement7()

    def mouvement0(self):
        self.setPosition(0, self.mob.get('speed'))

    def mouvement1(self):
        self.setPosition(0, self.mob.get('speed'))
        if self.lastShoot + self.fireRate <= self.getTimer():
            self.shoot()
            self.lastShoot = self.getTimer()

    def mouvement2(self):
        self.setPosition(self.mob.get('speed'), 0)

    def mouvement3(self):
        self.setPosition(self.mob.get('speed'), 0)
        if self.lastShoot + self.fireRate <= self.getTimer():
            self.shoot()
            self.lastShoot = self.getTimer()

    def mouvement4(self):
        self.setPosition(-self.mob.get('speed'), 0)

    def mouvement5(self):
        self.setPosition(-self.mob.get('speed'), 0)
        if self.lastShoot + self.fireRate <= self.getTimer():
            self.shoot()
            self.lastShoot = self.getTimer()

    def mouvement6(self):
        self.setPosition(self.mob.get('speed'), self.mob.get('speed'))

    def mouvement7(self):
        self.setPosition(self.mob.get('speed'), self.mob.get('speed'))
        if self.lastShoot + self.fireRate <= self.getTimer():
            self.shoot()
            self.lastShoot = self.getTimer()

    def mouvement8(self):
        self.setPosition(-self.mob.get('speed'), -self.mob.get('speed'))

    def mouvement9(self):
        self.setPosition(-self.mob.get('speed'), -self.mob.get('speed'))
        if self.lastShoot + self.fireRate <= self.getTimer():
            self.shoot()
            self.lastShoot = self.getTimer()

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

    # Methode lancé lors de la mort de l'ennemi
    #  on recupere sa position à l'instant et on change son image
    #  par l'image de la destruction.
    def destroy(self):
        self.isdestroy = True
        mobPos = self.image.Rect
        self.image = SpriteSheet(self.mob.get('destruction'), 4, 4, 2)
        self.Surface = self.image.Surface
        self.image.setPosition(mobPos[0] - (mobPos[2] /3), mobPos[1] - (mobPos[3] /3))
        self.Rect = self.getRect()
        self.image.setArea(0)
        self.area = self.image.getArea()
