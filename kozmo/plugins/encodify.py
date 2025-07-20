import sys
from base64 import b64encode
python2 = False
try:
    from io import StringIO
    from urllib.parse import quote_plus
except ImportError:
    import StringIO
    from urllib import quote_plus
    python2 = True

def octal(string):
    result = []
    for char in string:
        result.append('\%o' % ord(char))
    return ''.join(result)

def encode(string):
    print ('url: ' + quote_plus(string))
    print ('base64: ' + b64encode(string.encode('utf-8')).decode('utf-8'))
    try:
        print ('hex: ' + string.encode('utf-8').hex())
    except AttributeError:
        print ('hex: ' + string.encode('hex'))
    print ('octal: ' + octal(string))