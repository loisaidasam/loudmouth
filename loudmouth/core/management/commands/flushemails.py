# Command to flush emails

from django.core.management.base import NoArgsCommand

from loudmouth.core.models import IncomingEmail

class Command(NoArgsCommand):
	help = 'Flush all emails'
	
	def handle_noargs(self, **options):
		IncomingEmail.flush()