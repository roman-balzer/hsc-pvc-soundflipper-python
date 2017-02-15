import xmlrpc.client

class NetworkHandler:
    def __init__(self, configHandler):
        config = configHandler.getNetworkConfig()
        URI = config['uri']
        self.server = xmlrpc.client.ServerProxy(URI, allow_none=True)
        startNewGame()

    def send(self, points):
        self.server.addPoints(points)

    def startNewGame(self)
        self.server.newGame()

    def setMultiplicator(self, mult):
        self.server.setMultiplicator(mult)