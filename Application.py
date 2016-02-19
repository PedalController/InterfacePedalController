from controller.DataController import DataController
from controller.PluginsController import PluginsController

class Application:
    controllers = {}
    
    def __init__(self):
        DATA_PATH = "data/"
        
        self.controllers["data"] = DataController(DATA_PATH)
        self.controllers["plugins"] = PluginsController()