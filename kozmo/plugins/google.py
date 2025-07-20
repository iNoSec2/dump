from re import findall
from core.requester import requester

def googler(new, original, params, ip, hostname, inp):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept' : 'text/html, */*; q=0.01',
    'Accept-Encoding' : 'gzip',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection' : 'close'
    }
    response = requester('https://www.google.com/search', {'q' : inp[7:]}, headers, 'www.google.com', True)[2]
    matches = findall(r'<h3 class="r"><a href="(.*?)"', response)
    for match in matches:
        print (match.split('"')[0])