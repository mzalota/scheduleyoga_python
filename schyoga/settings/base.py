# Django settings for maxtest3 project.
from django.conf import global_settings
import warnings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

GRAPPELLI_ADMIN_TITLE = "ScheduleYoga.com Admin"


ADMINS = (
    ('Developer of SchYoga', 'mzalota@yahoo.com'),
)

MANAGERS = ADMINS

#Ignore numerous warnings about converting from native to timezone-aware DateTime object...
#http://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
#https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#code
#warnings.filterwarnings('ignore', r"DateTimeField received a naive datetime .*", RuntimeWarning, r'django\.db\.models\.fields')


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = "" #{"C:/Workspace/python/maxtest3/schyoga/static/"}

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'C:/Workspace/python/maxtest3/schyoga/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e8rq@3coa8_q+*x%kd%0!b*ly+ue#2(&ff4$pzfibbywm=ez%8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_facebook.middleware.FacebookMiddleware', #django_facebook.middleware.FacebookCanvasMiddleWare
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'schyoga.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'schyoga.wsgi.application'

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '../../../../..///', 'templates').replace('\\','/'),)


INSTALLED_APPS = (
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'django.contrib.flatpages',
    'schyoga',
    #'schyoga.admin',
    'django_facebook',
    'django.contrib.humanize',
    'sitetree', #https://django-sitetree.readthedocs.org/en/latest/quickstart.html
    'django_extensions',
    'cloudinary',
    'easy_maps',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

FACEBOOK_APP_ID = '168665979983590'
FACEBOOK_SECRET_KEY = '3902fc0c920f171bfd34bdde65415459'
FACEBOOK_APP_SECRET = ''

# Optionally set default permissions to request, e.g: ['email', 'user_about_me']
FACEBOOK_SCOPE = []

# And for local debugging, use one of the debug middlewares and set:
FACEBOOK_DEBUG_TOKEN = ''
FACEBOOK_DEBUG_UID = ''
FACEBOOK_DEBUG_COOKIE = ''
FACEBOOK_DEBUG_SIGNEDREQ = ''


#os.path.join(BASE_DIR, "static"),