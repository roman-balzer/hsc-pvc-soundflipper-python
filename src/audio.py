import configparser

def setup():
    # Get Config-Parameters
    config = configparser.ConfigParser()
    config.read('./src/config.ini')
    configParameters = config['audio']
    volume = int(configParameters['volume'])
    
