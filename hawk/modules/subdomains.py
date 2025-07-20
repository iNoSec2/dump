from core.values import var
from core.dorker import dorker
from urllib.parse import urlparse

meta = {
	'author' : 'Somdev Sangwan',
	'description' : 'find subdomains',
	'options' : {
		'domain' : {
			'value' : 'example.com',
			'required' : 'yes',
			'description' : 'top level domain'
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

def subdomains():
	dork = 'site:*' + var['domain']' -inurl:www.' + var['domain']
	var['pages'] = 100
	results = dorker(dork)
	unique_subdomains = set()
	for result in results:
		url = results[result]['url']
		subdomain = urlparse(url).netloc
		if ('.' + var['domain']) in subdomain:
			unique_subdomains.add(subdomain)
	for subdomain in unique_subdomains:
		print(subdomain)
