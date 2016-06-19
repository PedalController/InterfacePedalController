Registro = {}


def register(className):
    def decorator(method):
        #print("Registred:", method.__name__)
        if className not in Registro:
            Registro[className] = {"methods" : {}}

        Registro[className]["methods"][method.__name__] = {}

        def call(self, *args, **kwargs):
            key = '-'.join(sorted(kwargs.keys()))

            try:
                funcCallable = Registro[className]["methods"][method.__name__][key]
            except KeyError:
                funcCallable = lambda *args, **kwargs: (_ for _ in ()).throw(KeyError('Method not registred: ' + key))

            return method(self, funcCallable, *args, **kwargs)

        return call
    return decorator


def verb(name, className):
    #print("Verb:", name)
    def decorator(method):
        arguments = method.__code__.co_varnames[:method.__code__.co_argcount]
        arguments = sorted(arguments)
        arguments.remove('self')

        arguments = '-'.join(arguments)

        Registro[className]["methods"][name][arguments] = method

        #print(" + :", method.__name__, arguments)

        def call(self, *args, **kwargs):
            return method(self, *args, **kwargs)
        return call
    return decorator

'''
Python 3 (interrogacao)

import inspect

def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__ # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
        )
        if isinstance(cls, type):
            return cls
    return None
'#''

'#''
EXAMPLE
#''#'
class AlgumHandler:
    hue = "br"

    @register('AlgumHandler')
    def get(self, function, *args, **kwargs):
        result = function(self, *args, **kwargs)
        print(function.__name__, "returned", result)

    @verb("get", 'AlgumHandler')
    def bola(self, valor):
        print("Bola!", valor)
        return valor + 2

    @verb("get", 'AlgumHandler')
    def calsabre(self, valor, macarronada = "2"):
        print("Calsabre!", valor, macarronada)
        return valor + 5

handler = AlgumHandler()
handler.get(valor=3)
handler.get(macarronada="22", valor=3)
handler.get(valor=6, macarronada="8")

#print(AlgumHandler().bola(3))
#'''