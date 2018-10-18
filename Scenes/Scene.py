import random
from Components.Player import *
from Components.Mob import *
from Components.Projectile import *
from Components.Text import *
from Components.Image import *
from Components.UI import *
from Components.Bonus import *
from Components.Level import *
from Components.Config import *

class Scene:

    def __init__(self, screen, level):

        self.level = Level(level)
        self.config = Config("options")
        self.screen = screen
        self.background = Image(self.level.getBackground())

        self.y = 0          # Position pour le defilement du fond
        self.pause = False  # Valeur signifiant la pause des evenements
        self.option = False # Valeur signifiant l'ouverture du menu option
        self.end = False    # Valeur signifiant la fin de la partie
        self.buttons = {}
        self.timer = pygame.time.get_ticks()

        #Attributs liés au joueur
        playerDatas = self.level.getPlayer().get('sprite')
        self.init_player(playerDatas.get('image'), playerDatas.get('row'), playerDatas.get('column'), playerDatas.get('miss'))

        # Attributs liés aux ennemies
        self.ennemiNumber = self.level.getEnnemiNumber()
        self.ennemies = []
        self.ennemiesDead = {}

        # Attributs liés aux bonus
        self.bonus = []

        # Attributs liés aux textes (score / vies)
        self.score = Text()
        self.score.write('Score: %d' % self.player.score, Color(255, 255, 255))
        self.score.setPosition(6, 6)

        self.song = pygame.mixer.Sound(self.level.getMusic())

        if not self.config.getSong()['musicMuted']:
            self.song.play(1).set_volume(0.5)

    # Méthode appelant une nouvelle valeur joueur. Et le positionne par defaut
    def init_player(self, sprite, column, row, miss):
        self.player = Player(sprite, column, row, miss)
        self.player.setPosition((self.screen.width - self.player.width) /2, (self.screen.height - self.player.height) - 100)
        self.player.setArea()

    # Méthode d'appel des évènements de la scene
    def events(self):
        if not self.pause: # Si le jeu tourne ->
            self.player.events()
            self.player.shootEvent()
            self.mobAppear()
            self.newBonus()
            self.collision()
            for mob in self.ennemies:
                mob.events()
                if mob.isdestroy:
                    mob.setArea()
                if mob.checkIfOut() and mob.isHostile:
                    self.player.destroyed = True
                    self.Pause(True, False)
                elif mob.checkIfOut() and not mob.isHostile:
                    self.ennemies.remove(mob)
            for bonus in self.bonus:
                bonus.setArea()
                bonus.linearWalk()

            # Detecte la fin de la partie
            if self.getTimer() >= self.level.getTime() and len(self.ennemies) == 0:
                self.end = True
                self.Pause(False, True)

    # Méthode permettant le deplacement du fond de la scene
    def bcgScroll(self, pause = False):
        self.rel_y = self.y % self.background.Rect.height
        self.screen.blit(self.background.Surface, (0, self.rel_y - self.background.Rect.height))
        if (self.rel_y > -self.screen.Surface.get_height()):
            self.screen.blit(self.background.Surface, (0, self.rel_y))
            if not pause:
                self.y += 1

    # Méthode de vérification des collisions + gestion de celle-ci
    def collision(self):
        for mob in self.ennemies:
            # Si l'ennemis rencontre le joueur
            if mob.getRect().colliderect(self.player.image.Rect) and not mob.isdestroy:
                if not self.player.destroyed:
                    self.player.destroy(self.level.getPlayer()['destruction'])
                    self.Pause(True, True)

            # Si un tir du joueur rencontre l'ennemi
            for tir in self.player.tirs:
                if mob.getRect().colliderect(tir.getRect()) and not mob.isdestroy:
                    self.player.tirs.remove(tir)
                    self.player.addScore(5)
                    self.ennemiesDead[mob] = self.getTimer()
                    self.ennemiNumber -= 1
                    if not mob.isdestroy:
                        mob.destroy()

            # Si un tir ennemi rencontre un joueur
            for tir in mob.tirs:
                if self.player.getRect().colliderect(tir.getRect()) and not self.player.destroyed:
                    if not self.player.destroyed:
                        self.player.destroy(self.level.getPlayer()['destruction'])
                        self.Pause(True, True)

            # Si un ennemi est mort depuis un moment
            if mob.isdestroy and self.ennemiesDead[mob] + mob.getDepopTime() <= self.getTimer():
                del self.ennemiesDead[mob]
                self.ennemies.remove(mob)

        for bonus in self.bonus:
            # Si un bonus rencontre le joueur
            if bonus.getRect().colliderect(self.player.image.Rect):
                self.player.addScore(50)
                self.bonus.remove(bonus)

    # Méthode gerant l'affichage des elements sur la scène
    def display(self):
        if not self.pause:
            self.bcgScroll()
        else:
            self.bcgScroll(True)

        for bonus in self.bonus:
            self.screen.blit_area(bonus)

        for ennemi in self.ennemies:
            if ennemi.isdestroy:
                self.screen.blit_area(ennemi)
            else:
                for ennemiTir in ennemi.tirs:
                    self.screen.blit_area(ennemiTir)
                self.screen.blit(ennemi)

        for tir in self.player.tirs:
            self.screen.blit_area(tir)
        self.score.write('Score: %d' % self.player.score, Color(255, 255, 255))
        self.screen.blit(self.score, 0, 1)
        self.screen.blit_area(self.player)
        if self.pause and self.end and not self.player.destroyed:
            self.Pause(False, True)
            self.score.write('%d' % self.player.score, Color(255,255,255))
            self.score.setPosition(244, 100)
            self.screen.blit(self.score, 0, 1)
        elif self.pause and not self.end and self.player.destroyed:
            self.Pause(True, False)
        elif self.pause and not self.end and not self.player.destroyed:
            self.Pause(False, False)
        if self.option:
            self.options()

    def mobAppear(self):
        for ennemi in self.level.getEnnemis():
            spawnTimes = ennemi.get('spawns')
            for i in spawnTimes:
                time = self.getTimer()
                for y in i.get('time'):
                    if time >= y:
                        for z in range(i.get("number")):
                            mob = Mob(ennemi)
                            mob.setTimer(self.timer)
                            posx, posy = i.get("positions")[z-1].split(' ')
                            mob.setPosition(int(posx), int(posy))
                            mob.patterns = i.get("patterns")
                            self.ennemies.append(mob)
                        i.get("time").remove(y)

    # Méthode permettant la mise en pause ou l'arrêt du jeu en cours
    def Pause(self, dead, end):
        if not self.pause:
            self.pause = True
        UI.pauseMenu(self, dead, end)

    #Méthode permettant l'affichage de la fenêtre des options
    def options(self, close = False):
        if not close:
            if not self.option:
                self.option = True
                self.buttons[4] = pygame.Rect(351, 194, 16, 16)
                self.buttons[5] = pygame.Rect(126, 376, 16, 16)
                self.buttons[6] = pygame.Rect(126, 421, 16, 16)
            UI.optionMenu(self, self.config)
        else:
            self.option = False
            self.buttons = {}

    def setMusicConf(self):
        self.config.setSongConf('musicMuted')
        if self.config.getSong()['musicMuted']:
            self.song.stop()
        else:
            self.song.play(1).set_volume(0.5)

    def setSoundConf(self):
        self.config.setSongConf('soundMuted')
        if self.config.getSong()['soundMuted']:
            Player.playSound = False
            Projectile.playSound = False
        else:
            Player.playSound = True
            Projectile.playSound = True

    # Méthode permettant la reprise du jeu
    def Resume(self):
        if (self.pause and not self.player.destroyed) and (self.pause and not self.end):
            self.pause = False
            self.timer = pygame.time.get_ticks()
        else:
            self.quit()
            self.__init__(self.screen)

    # Méthode gérant l'apparition des bonus de point, selon un taux d'apparition
    def newBonus(self):
        x = random.randint(1, 1500);
        if x == 1:
            bonus = Bonus()
            position = random.randint(0, self.screen.Surface.get_width() - bonus.Surface.get_width())
            bonus.setPosition(position, -bonus.Surface.get_height())
            self.bonus.append(bonus)

    # Méthode retournant sur quel bouton le joueur clique
    def checkButton(self, mousePos):
        return UI.checkButton(self.buttons, mousePos)

    def getTimer(self):
        return pygame.time.get_ticks() - self.timer

    def quit(self):
        self.song.stop()
        self.screen.Surface.fill(Color(0,0,0))
