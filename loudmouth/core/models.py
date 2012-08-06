# General
import email.utils as email_utils
import logging
import operator
import time

# Library
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

# Project
from loudmouth.core.mailgrabber.imap import MailGrabberImap
from loudmouth.core.models_static import *


# Environment
logging.basicConfig(level = settings.LOGGER_LEVEL)
logger = logging.getLogger(__name__)


class EmailThread(models.Model):
	external_id = models.CharField(max_length=255, unique=True)


'''
Experiencing character encoding issues... 

Trying this:
mysql> ALTER TABLE core_incomingemail 
MODIFY COLUMN `title` VARCHAR(255)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, 
MODIFY COLUMN `summary` longtext  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ;

Unsuccessful. Gonna go with this:
summary = input.encode('unicode_escape')

Just need to remember to do this on output:
summary.decode('unicode_escape')

Solutions via: http://stackoverflow.com/questions/2108824/mysql-incorrect-string-value-error-when-save-unicode-string-in-django
'''

class IncomingEmail(models.Model):
	external_id = models.CharField(max_length=255, unique=True)
	thread = models.ForeignKey(EmailThread)
	on_email_list = models.BooleanField()
	timestamp = models.DateTimeField()
	title = models.CharField(max_length=255)
	author_name = models.CharField(max_length=255)
	author_email = models.CharField(max_length=255)
	summary = models.TextField()
	
	# Decided we're not gonna store this for now
	#raw_message = models.TextField()

	
	@staticmethod
	def flush():
		logger.info("IncomingEmail::flush() started...")
		
		logger.info("Grabbing all new emails via IMAP...")
		time_start = time.time()
		mg = MailGrabberImap(settings.LOGGER_EMAIL, settings.LOGGER_PASSWORD)
		
		# TODO: figure this out - it ain't working right now (maybe due to timezones?)
#		all_recent = IncomingEmail.objects.all().order_by('-timestamp')
#		if len(all_recent):
#			since_id = all_recent[0].external_id
#		else:
#			since_id = None
		since_id = None
		
		msgs = mg.grabNewMessages(since_id = since_id)
		
		time_elapsed = time.time() - time_start
		logger.info("Grabbed %i email%s in %0.2f seconds" % (len(msgs), (len(msgs) == 1 and '' or 's'), time_elapsed))
		
		email_lists = settings.EMAIL_LISTS
		
		if len(msgs):
			logger.info("Saving to the DB...")
			for msg in msgs:
				# Double check that we're not creating a dupe
				try:
					IncomingEmail.objects.get(external_id = msg['msg_id'])
					continue
				except IncomingEmail.DoesNotExist:
					pass
				
				try:
					thread = EmailThread.objects.get(external_id = msg['thread_id'])
				except EmailThread.DoesNotExist:
					thread = EmailThread.objects.create(external_id = msg['thread_id'])
				
				on_email_list = False
				recipients = msg['tos'] + msg['ccs']
				for email_tuple in recipients:
					if email_tuple[1] in email_lists:
						on_email_list = True
						break
				
				incoming_email = IncomingEmail.objects.create(
					external_id = msg['msg_id'],
					thread = thread,
					on_email_list = on_email_list,
					timestamp = msg['date'],
					title = msg['subject'],
					author_name = msg['from'][0],
					author_email = msg['from'][1],
					summary = msg['body'].decode('unicode_escape'),
					
					# Decided we're not gonna store this for now
					#raw_message = msg['raw'],
				)
		
		logger.info("IncomingEmail::flush() ended!")
	
	
	@staticmethod
	def get_user_emails(user, show_all=False, limit=None, offset=None):
		emails = []
		
		# TODO: implement limit/offset
		incoming_emails = IncomingEmail.objects.filter(on_email_list=True).order_by('-timestamp')
		for incoming_email in incoming_emails:
			try:
				email_rating = EmailRating.objects.get(user=user, email=incoming_email)
				if not show_all:
					continue
				rating = email_rating.rating
			except EmailRating.DoesNotExist:
				rating = None
			author_email = email_utils.formataddr((incoming_email.author_name, incoming_email.author_email))
			if len(incoming_email.summary) > 100:
				brief = incoming_email.summary[:100] + '...'
			else:
				brief = incoming_email.summary
			email = {
				'id': incoming_email.id,
				'title': incoming_email.title,
				'author': author_email,
				'brief': brief,
				'summary': incoming_email.summary, #.decode('unicode_escape'),
				'timestamp': incoming_email.timestamp,
				'rating': rating,
			}
			emails.append(email)
		
		return emails


class EmailRating(models.Model):
	user = models.ForeignKey(User)
	email = models.ForeignKey(IncomingEmail)
	rating = models.IntegerField(choices=EMAIL_RATINGS, default=EMAIL_RATING_OK)
	timestamp = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = (('user', 'email'),)
	
	
	@staticmethod
	def get_shamers():
		shamers = {}
		ratings = EmailRating.objects.all()
		for rating in ratings:
			shamers[rating.email.author_email] = shamers.get(rating.email.author_email, 0) + rating.rating
		return sorted(shamers.iteritems(), key=operator.itemgetter(1), reverse=True)
