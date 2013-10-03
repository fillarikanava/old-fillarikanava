DEBUG = False
TEMPLATE_DEBUG = True

ADMINS = (
    ('Hila Dev', 'dev+prod\100openfeedback.org'), # hide from google
    ('Reima Karhila', 'reima.karhila\100gmail.com')
)


MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = '$(hila_db)'
DATABASE_USER = '$(hila_db_user)'
DATABASE_PASSWORD = '$(hila_db_pass)'
DATABASE_HOST = ''
DATABASE_PORT = ''

MEDIA_URL = 'http://s.openfeedback.org/hila/prod/'


#MEDIA_ROOT = 'http://s.openfeedback.org/hila/prod/'
MEDIA_ROOT = '/home/hila/django/hila-prod/hila_webapp-trunk/media/' # ??? -rk

#ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

ADMIN_MEDIA_PREFIX = 'http://s.openfeedback.org/hila/prod/admin/'

GOOGLE_MAPS_KEY = '$(gmaps_api_key)'

TRACKER_HOME = '/opt/roundup/trackers/hilademo'
DJANGO_URL_PREFIX = ''

# http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

XAPIAN_DATABASE_HOME = TRACKER_HOME + '/db/text-index'
