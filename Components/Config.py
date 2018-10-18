import json

class Config:

    def __init__(self, name):
        self.name = name
        self.folder = 'Datas/'
        self.data = self.loadConf()

    def open(self, mode):
        fileName = self.folder + str(self.name) + ".json"
        if mode == 'r':
            with open(fileName, 'r') as file:
                self.file = file.read()
                file.close()
        elif mode == 'w':
            with open(fileName, 'w') as file:
                self.file = file.write(json.dumps(self.data, indent=2))
                file.close()

    def loadConf(self):
        self.open('r')
        return json.loads(self.file)

    def updateConf(self):
        self.open('w')

    def getSong(self):
        return self.data['song']

    def setSongConf(self, name):
        self.data = self.loadConf()
        song = self.getSong()
        if song[name] == True:
            song[name] = False
        else:
            song[name] = True
        self.updateConf()
        return song[name]
