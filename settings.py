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

# User account profiles
AUTH_PROFILE_MODULE = 'users.UserProfile'

# Login settings
LOGIN_URL = '/'

# Badge file path info
MAX_FILEPATH_LENGTH = 250

# Image file paths
BADGE_PREVIEW_PATH = 'uploads/badge_previews/'
BANNER_IMAGE_PATH = 'uploads/banners/'

# Session configuration
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Log out on browser close
SESSION_REMEMBER_DURATION = 1209600  # If we remember you, it lasts for 2 weeks

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'common': (
            'global/template.css',
            'css/styles.css',
            'css/uniform.default.css',
            'css/affiliates.css',
        ),
        'home': (
            'css/home.css',
        ),
        'user_profile': (
            'css/user_profile.css',
        ),
    },
    'js': {
        'common': (
            'js/libs/jquery-1.4.4.min.js',
            'global/js/nav-main.js',
            'js/libs/jquery.placeholder.min.js',
            'js/libs/jquery.uniform.min.js',
            'js/affiliates.js',
        ),
        'banners': (
            'js/libs/mustache.js',
            'js/banners.js',
        ),
    }
}

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'badges',
    'banners',
    'dumping_ground',
    'news',
    'users',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
]

# Add Jingo loader
TEMPLATE_LOADERS = [
    'jingo.Loader',
] + list(TEMPLATE_LOADERS)

JINGO_EXCLUDE_APPS = [
    'admin',
]

# Set up logging to send emails on 500 errors
LOGGING = {
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

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
