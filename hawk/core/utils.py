import importlib
from core.values import var

def get_module_info(name):
	module = importlib.import_module('modules.' + name)
	return module.meta

def load_options(module_name):
    options = get_module_info(module_name)['options']
    for option in options:
        var[option] = options[option]['value']

def reader(path, string=False):
    with open(path, 'r') as f:
        result = [line.rstrip(
                    '\n').encode('utf-8').decode('utf-8') for line in f]
    if string:
        return '\n'.join(result)
    else:
        return result
