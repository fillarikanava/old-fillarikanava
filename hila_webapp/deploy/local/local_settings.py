DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'hila_webapp'
DATABASE_USER = 'hila'
DATABASE_PASSWORD = 'hila'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin/media/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# Goto http://code.google.com/apis/maps/signup.html to generate one for your (local) domain
# Not required for localhost
#GOOGLE_MAPS_KEY =

# RoundUp tracker data directory, like "/roundup/trackers/hila"
TRACKER_HOME = '/opt/roundup/trackers/hilademo'

# http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''

XAPIAN_DATABASE_HOME = TRACKER_HOME + '/db/text-index'

DJANGO_URL_PREFIX = ''
