from util.Lv2Library import Lv2Library

class PluginsController:
    all = []

    def __init__(self):
        lib = Lv2Library()
        self.all = lib.plugins
    