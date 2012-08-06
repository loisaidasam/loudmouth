import feedparser
import urllib2

TOP_LEVEL_URL = "https://mail.google.com/mail"

class MailGrabber(object):
	opener = None
	
	def __init__(self, email, password):
		self.email = email
		self.password = password
	
	
	def _setup_opener(self):
		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		
		# Add the username and password.
		# If we knew the realm, we could use it instead of ``None``.
		password_mgr.add_password(None, TOP_LEVEL_URL, self.email, self.password)
		
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		
		# create "opener" (OpenerDirector instance)
		self.opener = urllib2.build_opener(handler)
	
		
	def grabNewMessages(self):
		if not self.opener:
			self._setup_opener()
		
		# use the opener to fetch a URL
		url = '%s/feed/atom' % TOP_LEVEL_URL
		raw_xml = self.opener.open(url)
		
		d = feedparser.parse(raw_xml)
		import pprint
		pprint.pprint(d)