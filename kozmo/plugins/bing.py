from re import findall
from core.requester import requester

def binger(new, original, params, ip, hostname, inp):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept' : 'text/html, */*; q=0.01',
    'Accept-Encoding' : 'gzip',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection' : 'close'
    }
    response = requester('https://www.bing.com/search', {'q' : inp[5:]}, headers, 'www.bing.com', True)[2]
    matches = findall(r'<a href="([^"]*)" h="', response.strip('\n'))[:-1]
    for match in matches:
        if match.startswith('http'):
            print (match)
