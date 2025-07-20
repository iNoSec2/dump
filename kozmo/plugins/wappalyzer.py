import json
from requests import get

def detect_tech(url):
    data = get('https://api.wappalyzer.com/lookup-basic/beta/?url=' + url).text
    jsoned_data = json.loads(data)
    technologies = []
    for one in jsoned_data:
        technologies.append(one['name'])
    return technologies