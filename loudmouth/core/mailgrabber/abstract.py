from loudmouth.core.mailgrabber import MailGrabberException


class MailGrabberAbstract(object):
	def __init__(self, email, password):
		if not email:
			raise MailGrabberException("No email provided to MailGrabber!")
		
		self.email = email
		self.password = password
	
	def grabNewMessages(self, since_id = None):
		raise MailGrabberException("grabNewMessages() not implemented")
