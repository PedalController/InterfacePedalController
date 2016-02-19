class Bank:
    data = {}

    def __init__(self, data):
        self.data = data
    
    def getParam(self, patch, effect, param):
        effect = self.getEffect(patch, effect)
        
        if effect is None:
            return None
        
        params = patch["params"]
        return self.get(params, param)

    def getEffect(self, patch, effect):
        patch = self.getPatch(patch)
        
        if patch is None:
            return None
        
        effects = patch["effects"]
        return self.get(effects, effect)
    
    def getPatch(self, patch):
        patches = self.data["patches"]
        
        return self.get(patches, patch)

    #@privatemethod
    def get(self, collection, index):
        hasElement = len(collection) >= index+1
        
        return collection[index] if hasElement else None