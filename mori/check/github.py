import re
import datetime
import requests

from shared.utils import log

def run(config):
	"""
	Check the GitHub activity of a user.
	"""
	url = f"https://api.github.com/users/{config['github_username']}/events/public"

	response = requests.get(url)
	
	if response.status_code != 200:
		log(__file__, 'Error fetching GitHub events')
		return 'error'
	
	events = response.json()
	
	if not events:
		log(__file__, 'No events found for user')
		return 'error'
	
	last_event_time = events[0]['created_at']
	last_event_date = datetime.datetime.strptime(last_event_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.UTC)
	
	if (datetime.datetime.now(datetime.UTC) - last_event_date).days > config['days_till_dead']:
		return 'dead'
	
	return 'alive'
