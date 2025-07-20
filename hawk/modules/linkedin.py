from core.values import var
from core.dorker import dorker

meta = {
	'author' : 'Somdev Sangwan',
	'description' : 'finds empolyees of a company on LinkedIn',
	'options' : {
		'company' : {
			'value' : 'Example Inc.',
			'required' : 'yes',
			'description' : 'target company'
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

def linkedin():
	dork = var['company'] + 'site:linkedin.com intext:Join to view full profile'
	var['pages'] = 100
	results = dorker(dork)
	for result in results:
		url = results[result]['url']
		if 'linkedin.com/in/' in url:
			print (url)
