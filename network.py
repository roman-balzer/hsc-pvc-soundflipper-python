import configparser
import xmlrpc.client

server = "Null"

def setup():
    global server
    # Get Config-Parameters
    config = configparser.ConfigParser()
    config.read('config.ini')
    configParameters = config['network']

    URI = configParameters['uri']
    server = xmlrpc.client.ServerProxy(URI)
    server.newGame()

def send(points):
    global server
    server.addPoints(points)