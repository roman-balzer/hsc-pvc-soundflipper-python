import configparser

class ConfigHandler:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./src/config.ini')
    def getGPIOConfig(self):
        return self.config['gpio']
    def getEarConfig(self):
        return self.config['ear']
    def getNetworkConfig(self):
        return self.config['network']
    def getVoiceConfig(self):
        return self.config['voice']
        