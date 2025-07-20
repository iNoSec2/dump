import types
from plugins.censys import censyss
from plugins.xsstrike import xsstriker

modules = [this for this in globals().values() if type(this) == types.FunctionType]

def pluginizer(new, original, params, ip, hostname, inp):
    name = inp.split(' ')[1]
    for module in modules:
        if name in str(module):
            module(new, original, params, ip, hostname, inp)