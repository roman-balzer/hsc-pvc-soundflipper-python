import xmlrpc.client

class NetworkHandler:
    def __init__(self, configHandler):
        print("NetworkHandler: Constructor")
        #config = configHandler.getNetworkConfig()
        #URI = config['uri']
        #self.server = xmlrpc.client.ServerProxy(URI, allow_none=True)
        #self.startNewGame()

    def send(self, points):
        horst = 1
        #self.server.addPoints(points)

    def startNewGame(self):
        horst = 1
        #self.server.newGame()

    def setMultiplicator(self, mult):
        horst = 1
        #self.server.setMultiplicator(mult)