'''
Some references for doing it this way:

https://support.google.com/mail/bin/answer.py?hl=en&answer=78799
http://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
http://docs.python.org/library/imaplib.html
http://stackoverflow.com/questions/1777264/using-python-imaplib-to-delete-an-email-from-gmail
http://stackoverflow.com/questions/5193707/use-imaplib-and-oauth-for-connection-with-gmail
http://code.google.com/apis/gmail/oauth/protocol.html
http://docs.python.org/library/email
http://imapclient.freshfoo.com/
'''

# General
import datetime
import email
import email.utils as email_utils
import imaplib
import re
import time

# Project
from loudmouth.core.mailgrabber import MailGrabberException
from loudmouth.core.mailgrabber.abstract import MailGrabberAbstract


BASE_URL = 'imap.gmail.com'


class MailGrabberImap(MailGrabberAbstract):
	
	M = None
	
	def _connect(self):
		self.M = imaplib.IMAP4_SSL(BASE_URL)
		self.M.login(self.email, self.password)
		self.M.list()
		
	
	def grabNewMessages(self, since_id = None):
		if not self.M:
			self._connect()

		# Out: list of "folders" aka labels in gmail.
		self.M.select("inbox") # connect to inbox.
	
		#result, data = self.M.search(None, "ALL")
		result, data = self.M.uid('search', None, "ALL")
	
	 	# data is a list.
		ids = data[0]
		# ids is a space separated string - reverse it to go from newest to oldest
		id_list = ids.split()
		id_list.reverse()
		
		msgs = []
	
		for id in id_list:
			# fetch the email body (RFC822) for the given ID
			#result, data = self.M.fetch(id, "(RFC822)") 
			result, data = self.M.uid('fetch', id, '(RFC822)')
	
			# here's the body, which is raw text of the whole email
			# including headers and alternate payloads
			raw_email = data[0][1]
			email_msg = email.message_from_string(raw_email)
			
			msg = {}
			
			msg['raw'] = raw_email
	
			# this becomes an organizational lifesaver once you have many results returned.
			result, data = self.M.uid('fetch', id, '(X-GM-THRID X-GM-MSGID)')
			result = re.search('X-GM-THRID (?P<thread_id>\d+) X-GM-MSGID (?P<msg_id>\d+)', data[0])
			if not result:
				raise MailGrabberException("Error finding thread id and message id! Data was %s" % data[0])
			
			msg['msg_id'] = str(result.groupdict()['msg_id'])
			msg['thread_id'] = str(result.groupdict()['thread_id'])
			
			if since_id is not None and msg['msg_id'] == since_id:
				break
			
			parsed_date = email_utils.parsedate(email_msg['Date'])
			msg['date'] = datetime.datetime.fromtimestamp(time.mktime(parsed_date))
			msg['from'] = email_utils.parseaddr(email_msg['From'])
			msg['subject'] = email_msg['Subject']
			
			msg['tos'] = email_utils.getaddresses(email_msg.get_all('To', []))
			msg['ccs'] = email_utils.getaddresses(email_msg.get_all('CC', []))
			
			if email_msg.is_multipart():
				msg['body'] = str(email_msg.get_payload(0).get_payload(decode=True))
			else:
				msg['body'] = str(email_msg.get_payload(decode=True))
			
			msgs.append(msg)
		
		# Reverse the order of the messages again so the oldest ones come first
		msgs.reverse()
		
		return msgs
