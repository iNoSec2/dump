import sys
from re import search
from base64 import b64decode
from core.colors import bad, good

if sys.version_info[0]==3:
    py_version = 3
    text_type = str
    binary_type = bytes
    from urllib.parse import unquote, urlencode
    from urllib.request import urlopen
else:
    py_version = 2
    text_type = unicode
    binary_type = str
    from urllib import urlopen, unquote, urlencode

decoded = []
currentstring = 0
loop = 0
listofstrings = []

def ensure_str(s, encoding='latin-1', errors='strict'):
    """Coerce *s* to `str`.
    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`
      - `bytes or bytearray` -> converted to str
    For Python 3:
      - `str` -> `str`
      - `bytes or bytearray` -> decoded to `str`
    """

    if not isinstance(s, (text_type, binary_type,bytearray)):
        raise TypeError("not expecting type '%s'" % type(s))
    if py_version == 2 and isinstance(s, text_type):
        s = s.encode(encoding, errors)
    elif py_version == 2 and isinstance(s, (binary_type,bytearray)):
        s = str(s)
    elif py_version == 3 and isinstance(s, (binary_type,bytearray)):
        s = s.decode(encoding, errors)
    return s

def check_ascii(s):
    """Sometimes the string is wrongly identified to be in someform of encoding and when it is decoded it gives gibberish this might to help to identify such wrong identification"""

    return all(ord(c) < 128 for c in s)

def Quit():
    global currentstring
    global decoded
    decoded = []
    if len(listofstrings) == currentstring:
        quit()
    else:
        currentstring += 1
        main(listofstrings[currentstring-1])

def SHA2(string, base):
    html = urlopen("http://md5decrypt.net/Api/api.php?hash="+string+"&hash_type=sha256&email=deanna_abshire@proxymail.eu&code=1152464b80a61728")
    string = html.read()
    string = ensure_str(string)
    if len(string) > 0:
        if string in decoded:
            Quit()
        print(good + ' sha2: %s' % string)
        decoded.append(string)
        decode(base, 'sha2')
        Quit()
    else:
        print(bad + ' Its a SHA2 Hash but I failed to crack it.')
        Quit()

def SHA1(string, base):
    data = urlencode({"auth":"8272hgt", "hash":string, "string":"","Submit":"Submit"})
    html = urlopen("http://hashcrack.com/index.php" , data)
    find = html.read()
    match = search (r'<span class=hervorheb2>[^<]*</span></div></TD>', find)
    if match:
        string = match.group().split('hervorheb2>')[1][:-18]
        string = ensure_str(string)
        if string in decoded:
            Quit()
        print(good + ' sha1: %s' % string)
        decoded.append(string)
        decode(base, 'sha1')
        Quit()
    else:
        print(bad + ' Its a SHA1 Hash but I failed to crack it.')
        Quit()

def MD5(string, base):
    url = "http://www.nitrxgen.net/md5db/" + string
    string = urlopen(url).read()
    string = ensure_str(string)
    if len(string) > 0:
        if string in decoded:
            Quit()
        print(good + ' md5: %s' % string)
        decoded.append(string)
        decode(base, 'md5')
        Quit()
    else:
        print(bad + ' Its a MD5 Hash but I failed to crack it.')
        Quit()

def fromchar(string, base):
        string = string.lower()
        string = string.strip('string.fromcharcode(').strip(')').strip(' ')
        jv_list = string.split(',')
        decoded = []
        for i in jv_list:
            i = i.replace(' ', '').replace('97', 'a').replace('98', 'b').replace('99', 'c').replace('100', 'd').replace('101', 'e').replace('102', 'f').replace('103', 'g').replace('104', 'h').replace('105', 'i').replace('106', 'j').replace('107', 'k').replace('108', 'l').replace('109', 'm').replace('110', 'n').replace('111', 'o').replace('112', 'p').replace('113', 'q').replace('114', 'r').replace('115', 's').replace('116', 't').replace('117', 'u').replace('118', 'v').replace('119', 'w').replace('120', 'x').replace('121', 'y').replace('122', 'z').replace('48', '0').replace('49', '1').replace('50', '2').replace('51', '3').replace('52', '4').replace('53', '5').replace('54', '6').replace('55', '7').replace('56', '8').replace('57', '9').replace('33', '!').replace('64', '@').replace('35', '#').replace('36', '$').replace('37', '%').replace('94', '^').replace('38', '&').replace('42', '*').replace('40', '(').replace('41', ')').replace('45', '-').replace('61', '=').replace('95', '_').replace('43', '+').replace('91', '[').replace('93', ']').replace('92', '\\').replace('59', ';').replace('39', '\'').replace('44', ',').replace('46', '.').replace('47', '/').replace('123', '{').replace('125', '}').replace('124', '|').replace('58', ':').replace('34', '"').replace('60', '<').replace('62', '>').replace('63', '?').replace('32', ' ').replace(',', '').replace('65', 'A').replace('66', 'B').replace('67', 'C').replace('68', 'D').replace('69', 'E').replace('70', 'F').replace('71', 'G').replace('72', 'H').replace('73', 'I').replace('74', 'J').replace('75', 'K').replace('76', 'L').replace('77', 'M').replace('78', 'N').replace('79', 'O').replace('80', 'P').replace('81', 'Q').replace('82', 'R').replace('83', 'S').replace('84', 'T').replace('85', 'U').replace('86', 'V').replace('87', 'W').replace('88', 'X').replace('89', 'Y').replace('90', 'Z').replace('32', ' ')
            decoded.append(i)
        string = ''.join(decoded)
        string = ensure_str(string)
        if string in decoded:
            Quit()
        print(good + ' fromchar: %s' % (string))
        decoded.append(string)
        decode(string, 'none')
        decode(base, 'jv_char')
        Quit()

def urle(string, base):
    string = unquote(string)
    string = ensure_str(string)
    if string in decoded:
        Quit()
    print(good + ' url: %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'url')
    Quit()

def hexenc(string, base):
    string = string.replace('0x', '')
    try:
        string = bytearray.fromhex(string)
    except:
        print (bad + ' Failed to detect the encoding.')
        if loop == 0:
            quit()
    string = ensure_str(string)

    if string in decoded:
        Quit()
    print(good + ' hex: %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'hexx')
    Quit()

def base64(string, base):
    string = b64decode(string)
    string = ensure_str(string)
    if string in decoded:
        Quit()
    print(good + ' base64: %s' % (string))
    decoded.append(string)
    decode(string, 'none')
    decode(base, 'b64')
    Quit()

def decimal(string, base):
    calculated = []
    string = ensure_str(string)
    string = string.replace('&#', '').replace(';', ' ')
    str_list = string.split(' ')
    for i in str_list:
        if i == ' ':
            pass
        else:
            try:
                i = int(i)
                calculated.append(chr(i))
            except:
                pass
    string = ''.join(calculated).encode('utf-8')
    if string in decoded:
        Quit()
    print(good + ' decimal: %s' % (string))
    decoded.append(string)

    decode(string, 'none')
    decode(base, 'deci')
    Quit()

def decode(string, stop):
    string = ensure_str(string)
    global loop
    if check_ascii(string):
        base = string
        sha2 = search(r'^([a-f0-9]{64})$', string)
        if sha2 and not sensitive and stop != 'sha2':
            SHA2(string, base)
        sha1 = search(r'^([a-f0-9]{40})$', string)
        if sha1 and not sensitive and stop != 'sha1':
            SHA1(string, base)
        md5 = search(r'^([a-f0-9]{32})$', string)
        if md5 and not sensitive and stop != 'md5':
            MD5(string, base)
        jv_char = search(r'\d*, \d*,', string)
        if jv_char and stop != 'jv_char':
            fromchar(string, base)
        url = search(r'%..%..+', string)
        if url and stop != 'url':
            urle(string, base)
        hexx = search(r'^(0x|0X)?[a-fA-F0-9]+$', string)
        if hexx and stop != 'hexx':
            hexenc(string, base)
        b64 = search(r'^[A-Za-z0-9+\/=]+$', string)
        if len(string) % 4 == 0 and b64 and stop != 'b64':
            base64(string, base)
        deci = search(r'&#.*;+', string)
        if deci and stop != 'deci':
            decimal(string, base)
        elif not decoded:
            print (bad + ' Failed to detect the encoding.')
            quit()
        loop += 1
        return 1

def dcode(string):
    decode(string, 'none')