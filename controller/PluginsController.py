from util.Lv2Library import Lv2Library

class PluginsController:
    plugins = []

    def __init__(self):
        lib = Lv2Library()
        self.plugins = lib.plugins
    