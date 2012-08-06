'''
Some references for doing it this way:

http://code.google.com/apis/gmail/docs/inbox_feed.html
http://packages.python.org/feedparser/introduction.html
'''

import feedparser
import urllib2

from loudmouth.core.mailgrabber import MailGrabberException
from loudmouth.core.mailgrabber.abstract import MailGrabberAbstract

TOP_LEVEL_URL = "https://mail.google.com/mail"

class MailGrabberAtom(MailGrabberAbstract):
	opener = None
		
	def _setup_opener(self):
		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		
		# Add the username and password.
		# If we knew the realm, we could use it instead of ``None``.
		password_mgr.add_password(None, TOP_LEVEL_URL, self.email, self.password)
		
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		
		# create "opener" (OpenerDirector instance)
		self.opener = urllib2.build_opener(handler)
	
		
	def grabNewMessages(self, since_id = None):
		if not self.opener:
			self._setup_opener()
		
		# use the opener to fetch a URL
		url = '%s/feed/atom' % TOP_LEVEL_URL
		raw_xml = self.opener.open(url)
		
		d = feedparser.parse(raw_xml)
		
		raise MailGrabberException("Need to finish writing this class!")
		
		import pprint
		pprint.pprint(d)
