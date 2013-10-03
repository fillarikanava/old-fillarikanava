# -*- coding: UTF-8 -*-
# Django settings for hila_webapp project.

import os

from local_settings import *



BASE_DIR = os.path.dirname(__file__)
# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'fi'

LANGUAGES=(
  ('fi', 'Finnish'),
  ('en', 'English'),
  ('sv', 'Svenska'),
  ('nl', 'Dutch'),
)

DEFAULT_LANGUAGE = 'fi'

DEFAULT_FROM_EMAIL = '"Fillarikanava" <webmaster@fillarikanava.hel.fi>'
ACCOUNT_ACTIVATION_DAYS = 14
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

# Facebook Connect related
FACEBOOK_API_KEY = '0d0420f8b2250d53a6fdbd49bc66b64a'
FACEBOOK_SECRET_KEY = '6927a02b9f77b55fc7888d7e2b5bca59'
FACEBOOK_UID = '785033956'

SITE_ID = 1
SITE_URL = 'http://fillarikanava.hel.fi'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))
#ADMIN_MEDIA_PREFIX = os.path.abspath(os.path.join(BASE_DIR, 'media'))+"/"


# Make this unique, and don't share it with anybody.
SECRET_KEY = '(2tl^46sjma$^^*z_1%l1=c6!7kvr0qbyn6bx=me00%gx8955('

AUTHENTICATION_BACKENDS = (
    'hila.facebookconnect.models.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
    'hila.auth.backends.RoundupBackend',
)

if 'FORCE_SCRIPT_NAME' in locals():
    LOGIN_URL = FORCE_SCRIPT_NAME + '/accounts/login/'
    LOGOUT_URL = FORCE_SCRIPT_NAME + '/accounts/logout/'
    LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME + '/accounts/profile/'

LOGIN_REDIRECT_URL = '/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'util.app_template_loader.load_template_source',
)

# Charset for HTML templates
FILE_CHARSET = 'utf-8'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'util.context_processors.settings',
    'util.context_processors.locale_constants',
    'multilingual.context_processors.multilingual',
    'django.core.context_processors.csrf',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'util.middleware.blockCrawlersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hila.facebookconnect.middleware.FacebookConnectMiddleware',
    'util.DefaultLanguageMiddleware.DefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'multilingual.middleware.DefaultLanguageMiddleware',
    'util.middleware.searchFilterMiddleware',
    'django.middleware.doc.XViewMiddleware',
#    'util.FacebookConnectMiddleware.FacebookConnectMiddleware',
    'util.middleware.JsonpMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'hila.organisation',
    'hila.public',
    'hila.public.report',
    'hila.public.archives',
    'hila.public.browse',
    'hila.public.front',
    'hila.public.report',
    'hila.public.widget',
    'hila.public.profiles',
    'hila.public.signup',
    'hila.facebookconnect',
    'hila.public.registration',
    'hila.api',
    'hila.api',
    'util.nomigrane',
    'ext',
    'captcha',
    'multilingual',
)


# XAPIAN SETTINGS
# default search depth for RT search
# Might have duplicates, so have to fetch some extra jujst to be sure
# will be fixed eventually... 
MAX_MATCHES_SEARCH=2000
MAX_MATCHES_SHOW=20
MAX_SEARCH_LIMIT=2000

# Stopwords. Do not index and do not search with these.
XAP_STOPWORDS=[u'juu', u'ei', u'myös', u'eli', u'eikä', u'myöskään', u'vai', u'onko', u'on',
           u'ilman', u'sekä', u'että', u'hän', u'minä', u'mä', u'se', u'sen', u'pitäisi',
           u'mun', u'ja']

# Xapian fields for 
XAPIAN_ISSUE_SCORE_VALUE = 1
XAPIAN_LATITUDE_VALUE = 4
XAPIAN_LONGITUDE_VALUE = 3

XAPIAN_X_COORD_FIELD=3
XAPIAN_Y_COORD_FIELD=4
XAPIAN_POSTAL_FIELD=5
XAPIAN_CREATED_FIELD=6
XAPIAN_MODIFIED_FIELD=7
XAPIAN_ARTIST_FIELD=8
XAPIAN_HAS_PICTURE_FIELD=9
XAPIAN_DATATYPE_FIELD=10
XAPIAN_ID_FIELD=11
XAPIAN_PARENT_ISSUE_FIELD=12
XAPIAN_PARENT_MESSAGE_FIELD=13
XAPIAN_STATUS_FIELD=14

JS_VERSION=17.6
