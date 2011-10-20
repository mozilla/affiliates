# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py
from funfactory.settings_base import *

# Logging
SYSLOG_TAG = "http_app_affiliates"  # Make this unique to your project.

# Language settings
PROD_LANGUAGES = ('de', 'en-US', 'es', 'fy-NL', 'nl', 'pl', 'pt-BR', 'sl',
                  'zh-TW')

# Email settings
DEFAULT_FROM_EMAIL = 'notifications@affiliates.mozilla.org'

# User accounts
AUTHENTICATION_BACKENDS = (
    'users.backends.EmailBackend',
)
AUTH_PROFILE_MODULE = 'users.UserProfile'
PASSWORD_RESET_TIMEOUT_DAYS = 2

# Login settings
LOGIN_VIEW_NAME = 'home'

# Badge file path info
MAX_FILEPATH_LENGTH = 250

# Image file paths
BADGE_PREVIEW_PATH = 'uploads/badge_previews/'
BANNER_IMAGE_PATH = 'uploads/banners/'

# CDN for absolutify
CDN_DOMAIN = None

# Paths that do not need a locale
SUPPORTED_NONLOCALES += ['link', 'admin']

# URL to redirect to on affiliate link errors
DEFAULT_AFFILIATE_LINK = 'http://mozilla.org'

# Leaderboard Display Size
LEADERBOARD_SIZE = 5

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Log out on browser close
SESSION_REMEMBER_DURATION = 1209600  # If we remember you, it lasts for 2 weeks

# Gravatar Settings
GRAVATAR_URL = 'https://secure.gravatar.com'
DEFAULT_GRAVATAR = MEDIA_URL + 'img/template/user-avatar.jpg'

# Set cookies to use secure flag
COOKIES_SECURE = True

# CacheMachine config
CACHE_COUNT_TIMEOUT = 60  # seconds, not too long.

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
        '404': (
            'css/404.css',
        ),
    },
    'js': {
        'common': (
            'js/libs/jquery-1.4.4.min.js',
            'global/js/nav-main.js',
            'js/libs/jquery.placeholder.min.js',
            'js/libs/jquery.uniform.min.js',
            'js/affiliates.js',
            'js/libs/webtrends.js',
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
    'shared',
    'news',
    'users',
    'smuggler',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [
    'commonware.middleware.StrictTransportMiddleware',
]

# Add Jingo loader
TEMPLATE_LOADERS = [
    'jingo.Loader',
] + list(TEMPLATE_LOADERS)

JINGO_EXCLUDE_APPS = [
    'admin',
    'smuggler',
]

# Set up logging to send emails on 500 errors
LOGGING = {
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'a': {
            'handlers': ['syslog'],
            'level': 'WARNING',
        },
    }
}

# Don't serve media by default
SERVE_MEDIA = False

DB_LOCALIZE = {
    'badges': {
        'Category': {
            'comments': ['Category of badges to choose from.'],
            'attrs': ['name']
        },
        'Subcategory': {
            'comments': ['Subcategory of badges to choose from.'],
            'attrs': ['name']
        },
        'Badge': {
            'comments': ['Badge that user can display on their website.'],
            'attrs': ['name']
        },
    },
    'banners': {
        'BannerImage': {
            'comments': ['Color for badge images.'],
            'attrs': ['color']
        },
    },
    'news': {
        'NewsItem': {
            'comments': ['Site news/notifications shown to users.'],
            'attrs': ['title', 'content']
        }
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
