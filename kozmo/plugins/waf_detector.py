import re
import requests
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from core.colors import bad, good

def detect_waf(url, headers):
    WAF_Name = False
    noise = quote_plus('<script>alert(1)</script>') #a payload which is noisy enough to provoke the WAF
    response = requests.get(url + '?xss=' + noise, headers=headers) # Opens the noise injected payload
    code = str(response.status_code)
    response_headers = str(response.headers)
    response_text = response.text.lower()
    if code[:1] != '2':
        if '406' == code or '501' == code: # if the http response code is 406/501
            WAF_Name = 'Mod_Security'
        elif 'wordfence' in response_text:
            WAF_Name = 'Wordfence'
        elif '999' == code: # if the http response code is 999
            WAF_Name = 'WebKnight'
        elif 'has disallowed characters' in response_text:
            WAF_Name = 'CodeIgniter'
        elif '<hr><center>nginx</center>' in response_text:
            WAF_Name = 'nginx'
        elif 'comodo' in response_text:
            WAF_Name = 'Comodo'
        elif 'sucuri' in response_text:
            WAF_Name = 'Sucuri'
        elif '419' == code: # if the http response code is 419
            WAF_Name = 'F5 BIG IP'
        elif 'barra' in response_headers:
            WAF_Name = 'Barracuda'
        elif re.search(r'cf[-|_]ray', response_headers):
            WAF_Name = 'Cloudflare'
        elif 'AkamaiGHost' in response_headers:
            WAF_Name = 'AkamaiGhost'
        elif '403' == code: # if the http response code is 403
            WAF_Name = 'Unknown'
    else:
        print('%s None' % good)
    if WAF_Name:
        print('%s %s' % (bad, WAF_Name))