from notify import email

def run(config):
	"""
	This function sends an email to the user to check if they are alive.
	It uses the email function from the notify module.
	"""

	email = config.get('email')
	subject = config.get('email_subject', 'Are you alive?')
	body = config.get('email_body', 'Please delete RISK.txt in your github repository if you are alive.')

	email(email, subject, body)