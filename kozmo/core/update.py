import os
from requests import get
from core.colors import info, good

def updater():
    print('%s Checking for updates' % run)
    changes = '''--exclude option to exclude urls with regex;minor refactor''' # Changes must be seperated by ;
    latest_commit = get('https://raw.githubusercontent.com/s0md3v/Kozmo/master/kozmo.py').text

    if changes not in latest_commit: # just a hack to see if a new version is available
        changelog = search(r"changes = '''(.*?)'''", latest_commit)
        changelog = changelog.group(1).split(';') # splitting the changes to form a list
        print('%s A new version of Kozmo is available.' % good)
        print('%s Changes:' % info)
        for change in changelog: # print changes
            print('%s>%s %s' % (green, end, change))

        current_path = os.getcwd().split('/') # if you know it, you know it
        folder = current_path[-1] # current directory name
        path = '/'.join(current_path) # current directory path
        choice = input('%s Would you like to update? [Y/n] ' % que).lower()

        if choice != 'n':
            print('%s Updating Kozmo' % run)
            os.system('git clone --quiet https://github.com/s0md3v/Kozmo %s' % (folder))
            os.system('cp -r %s/%s/* %s && rm -r %s/%s/ 2>/dev/null' % (path, folder, path, path, folder))
            print('%s Update successful!' % good)
    else:
        print('%s Kozmo is up to date!' % good)