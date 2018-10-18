from Scenes.Scene import *

class Water(Scene):

    def __init__(self, screen):
        super().__init__(screen, 2)
        self.player.set_animation_delay(200)
        self.player.changeFire(7)
        self.player.changeFireSong('Ressources/Songs/boulet.wav')
        Player.fireRate = 500
