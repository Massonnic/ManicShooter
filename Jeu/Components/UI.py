from pygame.locals import *
from Components.Image import *
from Components.Text import *

class UI: #Interface Utilisateur

    # Méthode gérant l'affichage du menu 'Pause / mort'
    def pauseMenu(scene, dead, end):

        # Instanciation des elements
        screen = scene.screen

        # Initialisation de la bonne image selon l'état du jeu en cours
        if not dead and not end:
            window = Image('Ressources/Sprites/Ui/pause.png', 1)
        else:
            window = Image('Ressources/Sprites/Ui/gameOver.png', 1)

        if end:
            scoreWindow = Image('Ressources/Sprites/Ui/score.png', 1)
            scoreWindow.setPosition(24, 8)

        # Assignation des rectangles pour les différents boutons
        resume = pygame.Rect(98, 235, 203, 50)
        options = pygame.Rect(98, 324, 203, 50)
        quit = pygame.Rect(98, 413, 203, 50)

        # Attribution des clefs selon les boutons
        scene.buttons[1] = resume
        scene.buttons[2] = options
        scene.buttons[3] = quit

        # Affichage des boutons avec leurs textes
        screen.blit(window, 0, 1)
        if end:
            screen.blit(scoreWindow, 0, 1)

    def optionMenu(scene, config):
        screen = scene.screen
        musicMuted = config.getSong()["musicMuted"]
        soundMuted = config.getSong()["soundMuted"]

        window = Image('Ressources/Sprites/Ui/option.png', 1)
        croix = Image('Ressources/Sprites/Ui/croix.png', 1)

        screen.blit(window, 0, 1)
        if musicMuted == True:
            croix.Rect = pygame.Rect(124, 366, 25, 25)
            screen.blit(croix, 0, 1)
        if soundMuted == True:
            croix.Rect = pygame.Rect(124, 411, 25, 25)
            screen.blit(croix, 0, 1)

    def credit(scene):
        screen = scene.screen
        window = Image('Ressources/Sprites/Ui/creditWindow.png', 1)

        screen.blit(window, 0, 1)

    # Méthodes permettant la disposition du texte au centre d'un conteneur
    def set_textual_button(surface, text, buttonColor, buttonPosition):
        x, y = buttonPosition
        surface.fill(buttonColor)
        surface.set_position(x, y)
        text.set_position(
            surface.Rect.left + ((surface.Surface.get_width() - text.Surface.get_width()) /2),
            surface.Rect.top + ((surface.Surface.get_height() - text.Surface.get_height()) /2))

    # Retourne la clef du bouton où le jouer à cliqué
    def checkButton(buttons, mousePos):
        lastKey = 0
        for key in buttons:
            if buttons[key].collidepoint(mousePos):
                lastKey = key
        return lastKey
