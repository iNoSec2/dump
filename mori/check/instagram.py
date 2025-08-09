import re
import datetime
import requests

from shared.utils import log

headers = {
	'X-IG-App-ID': '936619743392459'
}

def run(config):
	"""
	Check how long it has been since the user was last active on Instagram.
	"""
	url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={config['instagram_username']}"
	
	response = requests.get(url, headers=headers)
	
	if response.status_code != 200:
		log(__file__, 'Error fetching Instagram profile')
		return 'error'
	epochs = [int(i) for i in re.findall(r'"taken_at_timestamp":(\d+)', response.text)]
	if not epochs:
		log(__file__, 'No recent activity found')
		return 'error'
	last_active = max(epochs)
	if (datetime.datetime.now() - datetime.datetime.fromtimestamp(last_active)).days > config['days_till_dead']:
		return 'dead'
	return 'alive'
