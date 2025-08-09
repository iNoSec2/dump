import os
import sys

import act
import announce
import check
import warn

from shared.utils import get_config, get_modules, log


def check_all(config):
	"""
	Check if the user is alive by running all the checks in the check module.
	"""
	all_modules = get_modules(check)
	results = []
	for check_module in config['check']:
		if check_module not in all_modules:
			log('main', f'module check.{check_module} not found')
			continue
		module = all_modules[check_module]
		if not hasattr(module, 'run'):
			log('main', f'module check.{check_module} has no run function')
			continue
		try:
			result = module.run(config)
			results.append(result)
			print(f"check.{check_module} result: {result}")
		except Exception as e:
			log('main', f'Error running module check.{check_module}: {e}')
			results.append('error')
	
	if 'alive' in results:
		return 'alive'
	return 'dead'


def announce_all(config):
	"""
	Announce the user's death using all the announce modules.
	"""
	
	all_modules = get_modules(announce)
	for announce_module in config['announce']:
		if announce_module not in all_modules:
			log('main', f'module announce.{announce_module} not found')
			continue
		module = all_modules[announce_module]
		if not hasattr(module, 'run'):
			log('main', f'module announce.{announce_module} has no run function')
			continue
		try:
			module.run(config)
		except Exception as e:
			log('main', f'Error running module announce.{announce_module}: {e}')
			continue

def warn_all(config):
	"""
	Warn the user using all the warn modules.
	"""
	
	all_modules = get_modules(warn)
	for warn_module in config['warn']:
		if warn_module not in all_modules:
			log('main', f'module warn.{warn_module} not found')
			continue
		module = all_modules[warn_module]
		if not hasattr(module, 'run'):
			log('main', f'module warn.{warn_module} has no run function')
			continue
		try:
			module.run(config)
		except Exception as e:
			log('main', f'Error running module warn.{warn_module}: {e}')
			continue


def act_all(config):
	"""
	Perform any necessary actions using all the act modules.
	"""
	
	all_modules = get_modules(act)
	for act_module in config['act']:
		if act_module not in all_modules:
			log('main', f'module act.{act_module} not found')
			continue
		module = all_modules[act_module]
		if not hasattr(module, 'run'):
			log('main', f'module act.{act_module} has no run function')
			continue
		try:
			module.run(config)
		except Exception as e:
			log('main', f'Error running module act.{act_module}: {e}')
			continue


def main():
	"""
	This is program that runs once a day to check if the user is alive.
	It will check if the user is alive by checking the last time they were seen by methods in the check module.
	No acitivity for n days means death, it will send a notification to the user for confirmation using methods in the warn module.
	If the user doesn't respond to the notification, it will create a file named DELETE_IF_ALIVE.txt in the script's directory.
	If this file isn't deleted within a week, it will assume the user is dead.
	Once assumed dead, it will announce the user's death using methods in the announce module.
	Finally, it will run the act module to perform any actions defined by the user.

	Which functions are used from these modules and the cookies, usernames etc. required are defined in workflow.toml
	"""
	config = get_config("workflow.toml")
	if not config:
		log('main', "No valid config found")
		sys.exit(1)
	
	check_result = check_all(config)
	if check_result == 'alive':
		try:
			os.remove('DELETE_IF_ALIVE.txt')
		except FileNotFoundError:
			pass
		sys.exit("The user is alive, exiting.")

	# --- no activity in the last n days ----

	try:
		with open('DELETE_IF_ALIVE.txt', 'r') as f:
			content = f.read().strip()
			days_left = int(content)
			days_left -= 1
			if days_left > 0:
				with open('DELETE_IF_ALIVE.txt', 'w') as f:
					f.write(str(days_left))
				print(f"DELETE_IF_ALIVE.txt file updated, {days_left} days left until last rites.")
				warn_all(config)
				sys.exit('User has been warned, exiting.')
	except FileNotFoundError:
		pass

	# --- user didn't respond to warning ---

	print("The user is dead, performing last rites :(")
	announce_all(config)
	act_all(config)
	sys.exit("Rest in peace, exiting.")

if __name__ == "__main__":
	main()
