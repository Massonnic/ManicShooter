from Scenes.Scene import *

class Space(Scene):

    def __init__(self, screen):
        super().__init__(screen, 1)
        self.player.changeFireSong('Ressources/Songs/blaster.wav')
