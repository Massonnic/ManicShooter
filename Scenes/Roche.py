from Scenes.Scene import *

class Roche(Scene):

    restriction = 35

    def __init__(self, screen):
        super().__init__(screen, 3)
        self.player.set_animation_delay(100)
        self.player.changeFire(4)
        self.player.changeFireSong('Ressources/Songs/blaster.wav')
        Player.fireRate = 600
        self.player.double = True

    def events(self):
        if not self.pause: # Si le jeu tourne ->
            self.player.events(Roche.restriction)
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
            for bonus in self.bonus:
                bonus.setArea()
                bonus.linearWalk()

    def newBonus(self):
        x = random.randint(1, 1500)
        if x == 1:
            bonus = Bonus()
            position = random.randint(Roche.restriction, self.screen.Surface.get_width() - bonus.Surface.get_width() - Roche.restriction)
            bonus.setPosition(position, -bonus.Surface.get_height())
            self.bonus.append(bonus)
