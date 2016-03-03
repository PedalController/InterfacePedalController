class DeviceController:
    
    def __init__(self, app):
        self.app = app
    
    def setPatch(self, patch):
        print("Loading effects", patch["effects"])
        print("connecting", patch["connections"])

    def toggleStatusEffect(self, effect):
        print("Toggle status effect number:", effect)