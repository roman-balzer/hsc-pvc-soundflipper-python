import xmlrpc.client

class NetworkHandler:
    ## Initializes the network component.
    # Sets the GPIO pins (as in config file) and add callback function if pull-up detected.
    # @param self The object pointer.
    # @param configHandler The pointer to object of type configHandler
    def __init__(self, configHandler):
        print("NetworkHandler: Constructor")
        #config = configHandler.getNetworkConfig()
        #URI = config['uri']
        #self.server = xmlrpc.client.ServerProxy(URI, allow_none=True)
        #self.startNewGame()

    ## This function increments the score count by the provided amount in the parameter.
    # @param self - Object pointer
    # @param points - The value to add to the score
    def send(self, points):
        pass
        #self.server.addPoints(points)

    ## This function resets the game, and starts a new game
    # @param self - Obeject pointer
    def startNewGame(self):
        pass
        #self.server.newGame()

    ## This function sets a multiplicator, which multiplies the future incoming score
    # by the provided amount.
    # @param self - Object pointer
    # @param mult - The value by which future incoming score points should be multiplied
    def setMultiplicator(self, mult):
        pass
        #self.server.setMultiplicator(mult)