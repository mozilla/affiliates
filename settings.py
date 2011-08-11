# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Logging
SYSLOG_TAG = "http_app_playdoh"  # Make this unique to your project.

# Default language
LANGUAGE_CODE = 'en-US'

# Languages that Affiliates supports
AFFILIATES_LANGUAGES = ['en-US']

# Email settings
DEFAULT_FROM_EMAIL = 'notifications@affiliates.mozilla.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# User account profiles
AUTH_PROFILE_MODULE = 'users.UserProfile'

# Badge file path info
MAX_FILEPATH_LENGTH = 250

# Image file paths
BADGE_PREVIEW_PATH = 'uploads/badge_previews/'
BANNER_IMAGE_PATH = 'uploads/banners/'

# Port the server is running on (None in production)
SERVER_PORT = None

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'common': (
            'css/reset.css',
            'global/headerfooter.css',
            'css/main.css',
        ),
    },
    'js': {
        'common': (
            'js/libs/jquery-1.4.4.min.js',
            'global/menu.js',
        ),
        'banners': (
            'js/banners.js',
        ),
    }
}

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'badges',
    'banners',
    'users',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
]

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]
