import configparser
import xmlrpc.client

server = "Null"

def setup():
    global server
    # Get Config-Parameters
    config = configparser.ConfigParser()
    config.read('./src/config.ini')
    configParameters = config['network']

    URI = configParameters['uri']
    server = xmlrpc.client.ServerProxy(URI, allow_none=True)
    server.newGame()

def send(points):
    global server
    server.addPoints(points)

def startNewGame():
    global server
    server.newGame()

def setMultiplicator(mult):
    global server
    server.setMultiplicator(mult)