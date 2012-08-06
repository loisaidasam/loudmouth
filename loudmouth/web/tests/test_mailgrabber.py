
from django.conf import settings
from django.test import TestCase

import loudmouth.web.mailgrabber as mailgrabber


class MailGrabberTest(TestCase):
	def setUp(self):
		self.mg = mailgrabber.MailGrabber(settings.LOGGER_EMAIL, settings.LOGGER_PASSWORD)
	
	def test_simple(self):
		self.mg.grabNewMessages()