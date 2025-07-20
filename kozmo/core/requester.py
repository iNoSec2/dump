import random
import requests

def requester(url, data, headers, hostname, GET):
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']

    header = headers
    try:
        if header['User-Agent'] == '$':
            header['User-Agent'] = random.choice(user_agents)
        if header['Host'] == '$':
            header['Host'] = hostname
    except KeyError:
        pass
    if GET:
        response = requests.get(url, params=data, headers=header, verify=False)
        return [response.status_code, response.headers, response.text, response.elapsed.total_seconds()]
    else:
        response = requests.post(url, data=data, headers=header, verify=False)
        return [response.status_code, response.headers, response.text, response.elapsed.total_seconds()]