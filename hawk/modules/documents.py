from core.values import var
from core.dorker import dorker

meta = {
	'author' : 'Somdev Sangwan',
	'description' : 'find documents hosted on a domain',
	'options' : {
		'host' : {
			'value' : 'example.com',
			'required' : 'yes',
			'description' : 'target host'
		},
		'pages' : {
			'value' : 1,
			'required' : 'no',
			'description' : 'result pages to scrap'
		},
		'full' : {
			'value' : True,
			'required' : 'no',
			'description' : 'include omitted results'
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

def documents():
	dork = 'site:' + var['host'] + ' ext:(pdf |txt|xls|docx|csv)'
	results = dorker(dork)
	for result in results:
		print(results[result]['url'])
