import json
from io import TextIOBase

class Level:

    def __init__(self, level):
        self.folder = "Datas/"
        self.data = self.loadLevel(level)

    def loadLevel(self, level):
        file = open(self.folder + "level" + str(level) + ".json", 'r')
        return json.loads(file.read())

    def getBackground(self):
        return self.data['background']

    def getMusic(self):
        return self.data['music']

    def getTime(self):
        return self.data['time']

    def getEnnemiNumber(self):
        return self.data['ennemiNumber']

    def getEnnemis(self):
        return self.data['ennemis']

    def getPlayer(self):
        return self.data['player']
