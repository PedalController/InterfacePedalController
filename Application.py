from controller.BanksController import BanksController
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.PluginsController import PluginsController


class Application:
    controllers = {}
    
    def __init__(self):
        self.controllers[BanksController] = BanksController(self)
        self.controllers[CurrentController] = CurrentController(self)
        self.controllers[DeviceController] = DeviceController(self)
        self.controllers[PluginsController] = PluginsController()
        
        
    def dao(self, dao):
        DATA_PATH = "data/"
        
        return dao(DATA_PATH)
    
    def controller(self, controller):
        return self.controllers[controller]