from controller.BanksController import BanksController
from controller.PluginsController import PluginsController

class Application:
    controllers = {}
    
    def __init__(self):
        self.controllers[BanksController] = BanksController(self)
        self.controllers[PluginsController] = PluginsController()
        
    def dao(self, dao):
        DATA_PATH = "data/"
        
        return dao(DATA_PATH)
    
    def controller(self, controller):
        return self.controllers[controller]