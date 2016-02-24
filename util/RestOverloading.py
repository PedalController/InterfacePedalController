Registro = {
    "methods" : {}
}

def register(method):
    #print("Registred:", method.__name__)
    Registro["methods"][method.__name__] = {}

    def call(self, *args, **kwargs):
        key = '-'.join(sorted(kwargs.keys()))

        callable = Registro["methods"][method.__name__][key]
        return callable(self, *args, **kwargs)
        
    return call


def verb(name):
    #print("Verb:", name)
    def decorator(method):
        arguments = method.__code__.co_varnames[:method.__code__.co_argcount]
        arguments = sorted(arguments)
        arguments.remove('self')

        arguments = '-'.join(arguments)

        Registro["methods"][name][arguments] = method
        
        #print(" + :", method.__name__, arguments)
        
        def call(self, *args, **kwargs):
            return method(self, *args, **kwargs)
        return call
    return decorator

'''
EXAMPLE

class AlgumHandler:
    hue = "br"

    @register
    def get(self, *args, **kwargs):
        print("get?")
        pass

    @verb("get")
    def bola(self, valor):
        print("Bola!", valor)
        return valor + 2

    @verb("get")
    def calsabre(self, valor, macarronada = "2"):
        print("Calsabre!", valor, macarronada)
        return valor + 2

handler = AlgumHandler()
handler.get(valor=3)
handler.get(macarronada="22", valor=3)
handler.get(valor=3, macarronada="8")

#print(AlgumHandler().bola(3))
'''