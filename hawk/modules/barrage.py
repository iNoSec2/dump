import sys
import json
import concurrent.futures

from core.values import var
from core.goop import search
from core.utils import reader
from ui.colors import bad, end, blue, green, yellow

meta = {
    'author' : 'Somdev Sangwan',
    'description' : 'fire large number of dorks',
    'options' : {
        'host' : {
            'value' : 'example.com',
            'required' : 'no',
            'description' : 'target host'
        },
        'threads' : {
            'value' : 4,
            'required' : 'no',
            'description' : 'max concurrent requests'
        },
        'filter' : {
            'value' : '',
            'required' : 'no',
            'description' : 'custom search filter'
        }
    }
}

categories = {
    1 : 'Files Containing Juicy Info',
    2 : 'Files Containing Passwords',
    3 : 'Sensitive Directories',
    4 : 'Error Messages',
    5 : 'Pages Containing Login Portals',
    6 : 'Files Containing Usernames',
    7 : 'Vulnerable Servers',
    8 : 'Web Server Detection',
    9 : 'Advisories and Vulnerabilities',
    10 : 'Various Online Devices',
    11 : 'Network or Vulnerability Data',
    12 : 'Vulnerable Files',
    13 : 'Sensitive Online Shopping Info',
    14 : 'Footholds'
}

def barrage():
    focus = ''
    if var['host'] != 'example.com':
        focus = ' site:' + var['host']
    print ('Select an option:')
    for key, value in categories.items():
        print (str(key) + '. ' + value)
    print ('')
    while True:
        option = int(input('%soption? %s' % (blue, yellow)))
        print(end, end='\r')
        if option in range(1, 15):
            break
        else:
            print('%s Invalid option.' % bad)
    dorks = json.loads(reader(sys.path[0] + '/db/ghdb.json', string=True))
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    futures = (threadpool.submit(search, dork + focus, var['cookie'], full=True, barrage=True) for dork in dorks[categories[option]])
    for i in concurrent.futures.as_completed(futures):
        dork = i.result()
        if dork:
            print ('%s[%sSuccess%s]%s %s' % (green, end, green, end, dork))
