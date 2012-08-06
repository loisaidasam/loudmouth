# Django settings for loudmouth project.

import os
def next_to_this_file(additional_path, this_file = __file__):
	return os.path.join(os.path.dirname(os.path.abspath(this_file)), additional_path)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.',	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': '',					  		# Or path to database file if using sqlite3.
		'USER': '',					  		# Not used with sqlite3.
		'PASSWORD': '',				  		# Not used with sqlite3.
		'HOST': '',					  		# Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',					  		# Set to empty string for default. Not used with sqlite3.
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@l^73%xmq#e0_qe05b0e^2@3e+k=&a6x&*@9zogsz)mn#j@2-a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'loudmouth.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	next_to_this_file('templates'),
)

INSTALLED_APPS = (
	# Django
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	
	# Admin
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
	
	# Other libraries
	'registration',
	
	# Project
	'loudmouth.core',
	'loudmouth.web',
)

STATICFILES_DIRS = (next_to_this_file('smedia'), )

STATIC_ROOT = next_to_this_file('static')

STATIC_URL = '/static/'

TEST_EXCLUDE = (
	'registration',
)

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window;
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = ADMINS[0][1]
LOGIN_REDIRECT_URL = '/'

import logging
LOGGER_LEVEL = logging.INFO

try:
	from localsettings import *
except ImportError:
	print "You need to set up your localsettings.py file - try copying localsettings.py.template"
	raise
