import pygame
from pygame.locals import *
from Components.UI import *
from Components.Text import *
from Components.Image import *
from Components.Player import *
from Components.Projectile import *
from Components.Config import *

class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.config = Config('options')
        self.optionOpen = False
        self.creditOpen = False
        self.background = Image("Ressources/Sprites/Ui/menu.png")
        self.buttons = {}

        # Un paragraphe pour un bouton
        self.level1 = SpriteSheet("Ressources/Sprites/Ui/niveau1.png", 2, 1)
        self.level1.setPosition(30, 278)
        self.level1.setArea(0)
        self.buttons[1] = self.level1.Rect

        self.level2 = SpriteSheet("Ressources/Sprites/Ui/niveau2.png", 2, 1)
        self.level2.setPosition(85, 340)
        self.level2.setArea(0)
        self.buttons[2] = self.level2.Rect

        self.level3 = SpriteSheet("Ressources/Sprites/Ui/niveau3.png", 2, 1)
        self.level3.setPosition(30, 412)
        self.level3.setArea(0)
        self.buttons[3] = self.level3.Rect

        self.level4 = SpriteSheet("Ressources/Sprites/Ui/niveau4.png", 2, 1)
        self.level4.setPosition(85, 474)
        self.level4.setArea(0)
        self.buttons[4] = self.level4.Rect

        self.credit = SpriteSheet("Ressources/Sprites/Ui/credit.png", 2, 1)
        self.credit.setPosition(15, 635)
        self.credit.setArea(0)
        self.buttons[5] = self.credit.Rect

        self.option = Image("Ressources/Sprites/Ui/molette.png", 1)
        self.option.setPosition(351, 651)
        self.buttons[6] = self.option.Rect

        self.soundProcess()

    def checkButton(self, mousePos):
        return UI.checkButton(self.buttons, mousePos)

    def mouseOver(self):
        key = self.checkButton(pygame.mouse.get_pos())
        if key:
            if key == 1:
                self.level1.setArea(1)
            elif key == 2:
                self.level2.setArea(1)
            elif key == 3:
                self.level3.setArea(1)
            elif key == 4:
                self.level4.setArea(1)
        else:
            self.level1.setArea(0)
            self.level2.setArea(0)
            self.level3.setArea(0)
            self.level4.setArea(0)

    def options(self, close = False):
        if not close:
            if not self.optionOpen:
                self.optionOpen = True
                self.buttons[7] = pygame.Rect(351, 194, 16, 16)
                self.buttons[8] = pygame.Rect(126, 376, 16, 16)
                self.buttons[9] = pygame.Rect(126, 421, 16, 16)
            UI.optionMenu(self, self.config)
        else:
            self.optionOpen = False

    def creditWindow(self, close = False):
        if not close:
            if not self.creditOpen:
                self.creditOpen = True
                self.buttons[7] = pygame.Rect(351, 194, 16, 16)
            UI.credit(self)
        else:
            self.creditOpen = False

    def setMusicConf(self):
        self.config.setSongConf('musicMuted')

    def setSoundConf(self):
        self.config.setSongConf('soundMuted')
        self.soundProcess()

    def soundProcess(self):
        if self.config.getSong()['soundMuted']:
            Player.playSound = False
            Projectile.playSound = False
        else:
            Player.playSound = True
            Projectile.playSound = True

    def events(self):
        self.mouseOver()

    # Affichage de tous les boutons
    def display(self):
        self.screen.blit(self.background, 0, 1)
        self.screen.blit_area(self.level1)
        self.screen.blit_area(self.level2)
        self.screen.blit_area(self.level3)
        self.screen.blit_area(self.level4)
        self.screen.blit_area(self.credit)
        self.screen.blit(self.option, 0, 1)
        if self.optionOpen:
            self.options()
        elif self.creditOpen:
            self.creditWindow()

    def quit(self):
        self.screen.Surface.fill(Color(0, 0, 0))
