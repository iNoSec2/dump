import sys
import os
import platform

colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() # Get current version of OS
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed in mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')   # Enables the ANSI
if not colors:
    back = end = red = white = green = yellow = run = bad = good = info = que = ''
else:
    white = '\001\033[97m\002'
    green = '\001\033[92m\002'
    red = '\001\033[91m\002'
    blue = '\001\033[94m\002'
    yellow = '\001\033[93m\002'
    end = '\001\033[0m\002'
    back = '\001\033[7;91m\002'
    info = '\001\033[93m!\033[0m\002'
    que = '\001\033[94m?\033[0m\002'
    bad = '\001\033[91m-\033[0m\002'
    good = '\001\033[92m+\033[0m\002'
    run = '\001\033[97m*\033[0m\002'
