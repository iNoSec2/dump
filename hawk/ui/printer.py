from core.values import var
from ui.colors import end, blue, white, green
from core.utils import get_module_info

def show_banner():
    print ('\n\t\t%s-=%s нαωк 0.1-beta %s=-%s\n' % (white, green, white, end))

def show_help():
    print('')
    print('   Command\t\t\tDescription')
    print('   -------------------\t\t---------------------')
    print('   %-29sshow this help menu' % 'help')
    print('   %-29sexit the console' % 'exit/quit')
    print('   %-29sshow available modules' % 'show modules')
    print('   %-29sshow options for a module' % 'show options')
    print('   %-29smove back from the current context' % 'back')
    print('   %-29srun the selected module' % 'run')
    print('   %-29sassign value to a variable' % 'set')
    print('   %-29sreset value of a variable' % 'unset')
    print('')

def show_modules():
    print('')
    print('   Module\t\t\tDescription')
    print('   -------------------\t\t---------------------')
    for name in var['modules']:
        print('   %-29s%s' % (name, get_module_info(name)['description']))
    print('')

def show_options(module_name):
    options = get_module_info(module_name)['options']
    print('')
    print('   Option\tValue\t\tRequired\tDescription')
    print('   ------\t-----\t\t--------\t-----------')
    for option in options:
        print('   %-13s%-16s%-16s%s' % (option, var[option], options[option]['required'], options[option]['description']))
    print('')
