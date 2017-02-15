import configparser

## Encapsulates the functionality to read the config parameter from the config.ini file
class ConfigHandler:
    ## Constructor. Reads the config file config.ini in ./src folder.
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./src/config.ini')

    ## Returns the config parameters of section 'gpio'. 
    # This section should consist of all used GPIO-Pins in this programm.
    # @param self The object pointer.
    def getGPIOConfig(self):
        return self.config['gpio']

    ## Returns the config parameters of section 'ear'. 
    # This section should consist of all parameters which concern the ear component. 
    # The parameters should be the ones which the user should be able to adjust. 
    # Because they depend on the hardware or environment.
    def getEarConfig(self):
        return self.config['ear']

    ## Returns the config parameters of section 'network'. 
    # This section should consist of all parameters which concern the network communication.
    # For example the URI of the Server. 
    # The parameters should be the ones which the user should be able to adjust depending on his environment.
    def getNetworkConfig(self):
        return self.config['network']
    
    ## Returns the config parameters of section 'voice'. 
    # This section should consist of all parameters which concern the voice component. 
    # The parameters should be the ones which the user should be able to adjust. 
    # Because they depend on the hardware or environment.
    def getVoiceConfig(self):
        return self.config['voice']
        