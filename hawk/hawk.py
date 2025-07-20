# -*- coding: utf-8 -*-

import re
import sys
import pprint
import glob
import json
import readline
import importlib

from core.values import var
from ui.colors import end, red, bad, green, white, yellow
from core.utils import get_module_info, load_options, reader
from ui.printer import show_banner, show_help, show_modules, show_options

var['modules'] = [module.split('/')[-1].replace('.py', '') for module in glob.glob('./modules/*.py')]
commands = ['help', 'back', 'exit', 'quit', 'show modules', 'show options', 'use', 'set', 'unset', 'run']

show_banner()

def completer(text, state):
    options = [x for x in commands if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

var['path'] = ''
var['cookie'] = reader(sys.path[0] + '/db/cookie.txt', string=True)

if not var['cookie']:
	print('%s Cookie not found! Please paste your facebook cookie in /db/cookie.txt.' % bad)
	quit()

def initialize():
	while True:
		print (end, end='\r')
		user_input = input('%s%s>%s%s ' % (var['path'] + ' ' if var['path'] else '', green, end, yellow))
		print (end, end='\r')
		if user_input in ('exit', 'quit'):
			quit()
		elif user_input == 'back':
			var['path'] = ''
		elif user_input == 'show modules':
			show_modules()
		elif user_input.startswith('use'):
			wanted_module = re.sub(r'^use\s+', '', user_input)
			if wanted_module in var['modules']:
				var['wanted_module'] = wanted_module
				var['path'] = 'module' + green + '[' + red + wanted_module + green + ']' + end
				load_options(wanted_module)
			else:
				print('%s No such module.' % bad)
		elif user_input == 'show options':
			if var['path']:
				show_options(var['wanted_module'])
			else:
				print('%s No module selected.' % bad)
		elif user_input.startswith('set'):
			if var['path']:
				cleaned_input = re.sub(r'^set\s+', '', user_input).rstrip(' ')
				splitted = list(filter(None, cleaned_input.split(' ')))
				name = splitted[0]
				value = ' '.join(splitted[1:])
				var[name] = value
				print (name + ' => ' + value)
			else:
				print('%s No module selected.' % bad)
		elif user_input.startswith('unset'):
			cleaned_input = re.sub(r'^set\s+', '', user_input).rstrip(' ')
			var[cleaned_input] = ''
		elif user_input == 'run':
			var['stop_crawling'] = False
			if var['path']:
				wanted_module = var['wanted_module']
				function_string = 'modules.' + wanted_module + '.' + wanted_module
				mod_name, func_name = function_string.rsplit('.',1)
				mod = importlib.import_module(mod_name)
				func = getattr(mod, func_name)
				result = func()
			else:
				print('%s No module selected.' % bad)
		elif user_input == 'help':
			show_help()
		else:
			print('%s Invalid command.' % bad)

try:
	initialize()
except KeyboardInterrupt:
	exit('\033[0m')
