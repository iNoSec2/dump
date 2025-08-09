def run(config):
	"""
	This function sends a tweet to announce the user's death.
	"""

	tweet = config.get('tweet')
	if not tweet:
		return
