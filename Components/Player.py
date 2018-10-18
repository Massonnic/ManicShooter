from pygame.locals import *
from Components.Image import *
from Components.Projectile import *
pygame.mixer.init()

class Player:

    speed = 3
    fireRate = 250
    lastTicks = pygame.time.get_ticks()
    playSound = True

    def __init__(self, image, column, row, miss):
        self.image = SpriteSheet(image, column, row, miss)
        self.image.setArea(0)
        self.Surface = self.image.Surface
        self.width = self.image.width
        self.height = self.image.height
        self.area = self.image.getArea()
        self.score = 0
        self.speed = Player.speed
        self.tirs = [] # Liste des projectiles tirés par le joueur
        self.double = False
        self.fire = 3
        self.song = 'Ressources/Songs/tir.wav'

        self.destroyed = False # Est-ce que le joueur est détruit ?

        self.animationDelay = 30 #ms
        self.animationTimer = pygame.time.get_ticks()

        self.destructionSound = pygame.mixer.Sound('Ressources/Songs/explosion.wav')

    # Initialise la position du joueur
    def setPosition(self, x, y):
        self.image.setPosition(x, y)
        self.Rect = self.getRect()

    def getRect(self):
        return self.image.Rect

    def set_animation_delay(self, delay):
        self.animationDelay = delay

    # Initialise la valeur area, la zone à afficher dans une spritesheet
    def setArea(self):
        # Si le temps depuis le dernier appel + le delay sont toujours supérieur,
        #   on attend que le temps passe
        if self.animationTimer + self.animationDelay < pygame.time.get_ticks():
            self.image.currentFrame += 1
            if self.image.currentFrame >= self.image.number:
                #Si on depasse le nombre d'images dans la sprite, on revient à la premiere
                if not self.destroyed:
                    self.image.currentFrame = 0
                else:
                    self.image.currentFrame = self.image.number -1
            self.image.setArea(self.image.currentFrame)
            self.area = self.image.getArea()
            self.animationTimer = pygame.time.get_ticks()

    # Methode pour changer le projectile du joueur
    def changeFire(self, fire):
        self.fire = fire

    def changeFireSong(self, song):
        self.song = song

    # Effectue toutes les methodes d'evenement de l'objet
    def events(self, restriction = 0):
        self.checkKeyboard()
        self.checkIfOut(restriction)
        self.setArea()

    # Pour chaque projectiles on le fait avancer et on le suppr si il sort de
    #  la fenetre du jeu
    def shootEvent(self):
        for tir in self.tirs:
            tir.setArea()
            tir.setPosition(0, -self.speed)
            if not tir.isInWindow():
                self.tirs.remove(tir)

    # Création du projectile en jeu et stockage de l'objet
    #   dans un tableau rassemblant tous les projectiles du joueur
    def shoot(self, double):
        tir = Projectile(self.fire, self.song)
        tir.setPosition(self.image.Rect.left + ((self.width - tir.width) /2), self.image.Rect.top - tir.height)

        if double:
            tir2 = Projectile(self.fire, self.song)
            tir.setPosition(-((self.width - tir.width) /2) + 10, 0)
            tir2.setPosition(self.image.Rect.left + ((self.width - tir.width) /2) + ((self.width - tir.width) /2) - 10, self.image.Rect.top - tir.height)
            self.tirs.append(tir2)

        self.tirs.append(tir)

    # Vérifie si le joueur dépace de la fenêtre, si oui le remet au bord
    def checkIfOut(self, restriction):
        if self.image.Rect[0] < restriction:
            self.image.setPosition(-self.image.Rect[0] + restriction, 0)
        if self.image.Rect[0] > (400 - self.image.Rect[2]) - restriction:
            self.image.setPosition(-self.image.Rect[0] + (400 - self.image.Rect[2] - restriction), 0)
        self.Rect = self.getRect()


    # Vérifie si le joueur appuie sur certains
    #   boutons et effectue les manipulations adéquates
    def checkKeyboard(self):
        l_key = pygame.key.get_pressed()
        if l_key[K_RIGHT]:
            self.image.setPosition(Player.speed, 0)
        if l_key[K_LEFT]:
            self.image.setPosition(-Player.speed, 0)
        if l_key[K_SPACE]:
            if (Player.lastTicks + Player.fireRate) <= pygame.time.get_ticks():
                Player.lastTicks = pygame.time.get_ticks()
                self.shoot(self.double)

    # Initialise le score du joueur à une valeur donnée
    def setScore(self, number):
        self.score = number

    # Ajoute le nombre de points donné au score du joueur
    def addScore(self, number):
        self.score += number

    # Retire le nombre de points donné au score du joueur
    def remScore(self, number):
        self.score -= number

    # Methode lancé lors de la mort du joueur
    #  on recupere la position du joueur à l'instant et on change son image
    #  par l'image de la destruction.
    def destroy(self, image):
        playerPos = self.image.Rect
        self.image = SpriteSheet(image, 4, 4, 2)
        self.Surface = self.image.Surface
        self.image.setPosition(playerPos[0] - (playerPos[2] /2), playerPos[1] - (playerPos[3] /2))
        self.Rect = self.getRect()
        self.image.setArea(4)
        self.area = self.image.getArea()
        self.animationDelay = 60
        self.destroyed = True

        if Player.playSound:
            self.destructionSound.play().set_volume(0.5)
