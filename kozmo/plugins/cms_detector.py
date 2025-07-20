from re import search
from requests import get

def detect_cms(domain):
    response = get('https://whatcms.org/?s=%s' % domain).text
    match = search(r'<a href="/c/\w+" class="nowrap" title="\w+">(.*?)</a></div>', response)
    try:
        return match.group(1)
    except AttributeError:
        return False