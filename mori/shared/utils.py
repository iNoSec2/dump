import importlib
import pkgutil
import sys
import toml

def log(script, message):
	"""
	Log a message to the console.
	"""
	name = ".".join(script.split("/")[-2:]).replace(".py", "")
	if not name:
		print(f"[main] {message}", file=sys.stderr)
	else:
		print(f"[{name}] {message}", file=sys.stderr)

def get_config(config):
	"""
	Get the configuration from the config file.
	"""
	if not config:
		log(__file__, "No config file found")
		return {}
	
	if isinstance(config, str):
		config = toml.load(config)
	
	if not isinstance(config, dict):
		log(__file__, "Invalid config file format")
		return {}
	
	return config

def get_modules(category):
	"""
	Get all the modules in the given category
	"""
	check_modules = {}
	for _, name, _ in pkgutil.iter_modules(category.__path__):
		module = importlib.import_module(f'{category.__name__}.{name}')
		check_modules[name] = module
	return check_modules