import json
import tornado.escape

class Bank:
    data = {}

    def __init__(self, data):
        self.data = data
    
    '''==================================
    Property
    =================================='''
    
    @property
    def json(self):
        return self.data
    
    @json.setter
    def setJson(self, value):
        self.data = value
    
    @property
    def patches(self):
        return self.data["patches"]
    
    
    '''==================================
    Facade
    =================================='''
    
    def getParam(self, patch, effect, param):
        params = self.getParams(patch, effect)
        return self.get(params, param)
    
    def getParams(self, patch, effect):
        return self.getEffect(patch, effect)["params"]
    
    def addEffect(self, patch, effect):
        patch = self.getPatch(patch)
        patch["effects"].append(effect)
    
    def getEffect(self, patch, effect):
        effects = self.getEffects(patch)
        return self.get(effects, effect)    
    
    def getEffects(self, patch):
        return self.getPatch(patch)["effects"]
    
    def getPatch(self, patch):
        return self.get(self.patches, patch)

    def addPatch(self, patch):
        self.patches.append(patch)
    
    '''==================================
    Private
    =================================='''

    #@privatemethod
    def get(self, collection, index):
        hasElement = len(collection) >= index+1
        
        try:
            return collection[index]
        except IndexError:
            raise IndexError("Element not found")
        