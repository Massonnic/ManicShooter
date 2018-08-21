from Scenes.Scene import *

class Fire(Scene):

    def __init__(self, screen):
        super().__init__(screen, 2)
        self.player.changeFire("Ressources/Sprites/flamme.png")
