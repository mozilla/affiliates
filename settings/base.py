# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py
from funfactory.settings_base import *

# Logging
SYSLOG_TAG = "http_app_affiliates"  # Make this unique to your project.

# Language settings
PROD_LANGUAGES = ('cs', 'de', 'en-US', 'es', 'fr', 'fy-NL', 'hr', 'ko', 'nl',
                  'pl', 'pt-BR', 'ru', 'sk', 'sl', 'sq', 'sr', 'sr-LATN', 'tr',
                  'zh-TW')

# UPSTREAM: Change lazy_langs to search for locales in a case-insensitive
# manner.
def lazy_langs():
    from django.conf import settings
    from product_details import product_details

    available_langs = dict([(key.lower(), value) for key, value in
                            product_details.languages.items()])
    langs = DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    langs = [lang.lower() for lang in langs]

    return dict([(lang, available_langs[lang]['native'])
                 for lang in langs if lang in available_langs])

LANGUAGES = lazy(lazy_langs, dict)()


# List of valid country codes.
def lazy_countries():
    from product_details import product_details
    return product_details.get_regions('en-US')
COUNTRIES = lazy(lazy_countries, dict)()

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_DIR = path('lib/product_details_json')

# Email settings
DEFAULT_FROM_EMAIL = 'notifications@affiliates.mozilla.org'

# User accounts
AUTHENTICATION_BACKENDS = (
    'users.backends.EmailBackend',
    'browserid.backends.BrowserIDSessionBackend',
)
AUTH_PROFILE_MODULE = 'users.UserProfile'
PASSWORD_RESET_TIMEOUT_DAYS = 2

# BrowserID
BROWSERID_VERIFICATION_URL = 'https://browserid.org/verify'
BROWSERID_DISABLE_CERT_CHECK = False
BROWSERID_CREATE_USER = False
BROWSERID_LOCALES = [lang.lower() for lang in (
    'cs', 'de', 'en-US', 'es', 'fr', 'fy-NL', 'hr', 'nl', 'pl', 'pt-BR', 'sk',
    'sl', 'sq', 'sr', 'zh-TW'
    )]

# Login settings
LOGIN_VIEW_NAME = 'home'

# Badge file path info
MAX_FILEPATH_LENGTH = 250

# Image file paths
def LOCALE_IMAGE_PATH(instance, filename):
    return 'uploads/locale_images/%s/%s' % (instance.locale, filename)
BANNER_IMAGE_PATH = 'uploads/banners/'

# Default image for badge previews to fall back on
DEFAULT_BADGE_PREVIEW = MEDIA_URL + 'img/template/default-preview.png'

# CDN for absolutify
CDN_DOMAIN = None

# Paths that do not need a locale
SUPPORTED_NONLOCALES += ['link', 'admin', 'fb']

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

# Set up custom serializer and django-smuggler
SERIALIZATION_MODULES = {
    'json_files': 'shared.serializers.json_files',
}
SMUGGLER_FORMAT = 'json_files'

# Email subscription config
BASKET_URL = 'http://basket.mozilla.com'
BASKET_NEWSLETTER = 'affiliates'

# CSP Config
CSP_EXCLUDE_URL_PREFIXES = ('/admin',)
CSP_SCRIPT_SRC = (
    '\'self\'',
    'https://browserid.org',
    'https://login.persona.org',
    'https://statse.webtrendslive.com'
)
CSP_FRAME_SRC = (
    '\'self\'',
    'https://browserid.org',
    'https://login.persona.org'
)
CSP_IMG_SRC = (
    '\'self\'',
    'data:',
    'https://affiliates-cdn.mozilla.org',
    'https://statse.webtrendslive.com',
    'https://secure.gravatar.com',
    'https://graph.facebook.com',
    'https://*.fbcdn.net',
    'https://*.akamaihd.net',
)
CSP_FONT_SRC = (
    '\'self\'',
    'https://www.mozilla.org'
)

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'common': (
            'global/template.css',
            'css/styles.css',
            'css/uniform.default.css',
            'css/affiliates.css',
            'css/month_year_picker.css',
            'css/my_banners.css',
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
        'banners': (
            'css/banners.css',
        ),
        'persona-buttons': (
            'css/persona-buttons.css',
        ),

        # Facebook app
        'fb_base': (
            'css/facebook.css',
            'css/month_year_picker.css',
        ),
    },
    'js': {
        'common': (
            'js/libs/jquery-1.7.1.js',
            'js/libs/underscore.js',
            'global/js/nav-main.js',
            'js/libs/jquery.placeholder.min.js',
            'js/libs/jquery.uniform.min.js',
            'js/libs/spin.js',
            'js/month_year_picker.js',
            'js/affiliates.js',
            'js/libs/webtrends.js',
        ),
        'banners': (
            'js/libs/mustache.js',
            'js/banners.js',
        ),
        'browserid': (
            'js/browserid.js',
        ),

        # Facebook app
        'fb_common': (
            'js/libs/jquery-1.7.1.js',
            'js/libs/spin.js',
            'js/month_year_picker.js',
            'js/facebook/common.js',
        ),
        'fb_pre_auth_promo': (
            'js/facebook/pre_auth_promo.js',
        ),
        'fb_banner_share': (
            'js/libs/jquery-1.7.1.js',
            'js/facebook/banner_share.js',
        ),
        'fb_invite': (
            'js/libs/jquery-1.7.1.js',
            'js/facebook/invite.js',
        ),
        'fb_leaderboard': (
            'js/libs/jquery-1.7.1.js',
            'js/facebook/leaderboard.js',
        ),
        'fb_banner_create': (
            'js/facebook/banner_create.js',
        ),
        'fb_redirect': (
            'js/libs/jquery-1.7.1.js',
            'js/facebook/redirect.js',
        ),
        'fb_banner_list': (
            'js/facebook/banner_delete.js',
        ),
    }
}

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'stats',
    'badges',
    'banners',
    'browserid',
    'facebook',
    'shared',
    'news',
    'users',

    'csp',
    'django_extensions',
    'django_statsd',
    'smuggler',
    'cronjobs',
    'south',
    'django_browserid',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
]

MIDDLEWARE_CLASSES = [
    # Add timing middleware first to get accurate timings.
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
] + list(MIDDLEWARE_CLASSES) + [
    'commonware.middleware.StrictTransportMiddleware',
    'commonware.middleware.ScrubRequestOnException',
    'csp.middleware.CSPMiddleware',
    'shared.middleware.PrivacyMiddleware',
]

# Facebook auth middleware needs to come after AuthMiddleware but before
# session-csrf middleware so that it will generate csrf tokens.
auth_index = MIDDLEWARE_CLASSES.index('django.contrib.auth.middleware.AuthenticationMiddleware')
MIDDLEWARE_CLASSES.insert(auth_index + 1, 'facebook.middleware.FacebookAuthenticationMiddleware')

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'shared.context_processors.common',
    'shared.context_processors.l10n',
    'shared.context_processors.month_year_picker',
    'facebook.context_processors.app_context',
]

# Add Jingo loader
TEMPLATE_LOADERS = [
    'jingo.Loader',
] + list(TEMPLATE_LOADERS)

JINGO_EXCLUDE_APPS = [
    'admin',
    'smuggler',
    'stats',
    'fb',
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

SOUTH_TESTS_MIGRATE = False  # Disable migrations for tests.

# Extra places to look for fixtures
FIXTURE_DIRS = (
    path('fixtures'),
)

# Activate statsd patches to time database and cache hits.
STATSD_PATCHES = [
    'django_statsd.patches.db',
    'django_statsd.patches.cache',
]

# Bug 719522
# Old Firefox get redirected there
FIREFOX_UPGRADE_REDIRECT = 'http://www.mozilla.org/firefox/speed/?WT.mc_id=affaupgrade1&WT.mc_ev=click'

# Bug 719522
# List of hashes of banner images for upgrade campaign
# NOTE: This list should only contain banners ready to go on production. If you
# want to add more banners locally, you can override this setting in local.py.
BANNERS_HASH = [
    '1fe924573d36f18d1430311ecc892977ad0bd6a1',  # en-US Tall
    'ab1148a01251db077970056468c9b19c5f9e01f7',  # en-US Box
    '15413d5031733cefed719c624c30c6a20d337505',  # cs Tall
    'cd817e1604c5319499c2a226e13487d74efd713d',  # cs Box
    'a4de4d7b527b5b13eba9c9616d6f7d07db22ae2f',  # es-ES Tall
    '7cefdb2af229483dc68798e404457f563930a31c',  # es-ES Box
]

# Settings for Affiliates Facebook app
FACEBOOK_PERMISSIONS = ''
FACEBOOK_LOCALES = ('en-us', 'de', 'es', 'fr', 'nl', 'pl', 'pt-br', 'sq',
                    'zh-tw')
FACEBOOK_DOWNLOAD_URL = 'https://www.mozilla.org/firefox'
FACEBOOK_MAILING_LIST = 'mozilla-and-you'

FACEBOOK_CLICK_GOAL = 50
FACEBOOK_CLICK_GOAL_EMAIL = 'affiliates@mozilla.org'

FACEBOOK_BANNER_IMAGE_PATH = 'uploads/facebook/banners/'
FACEBOOK_BANNER_INSTANCE_IMAGE_PATH = 'uploads/facebook/banner_instances/'


# Coordinates for the Facebook profile image when pasted onto a banner image.
# Format is (left, upper)
FACEBOOK_CUSTOM_IMG_COORDS = (235, 151)
FACEBOOK_CUSTOM_IMG_BORDER = {'width': 3, 'color': '#ccc'}

# Period of time that an account link activation link is valid, in seconds.
FACEBOOK_LINK_DELAY = 60 * 60 * 24 * 2  # 2 Days


# FACEBOOK_APP_URL is lazily evaluated because it depends on the namespace
# setting in local settings.
def facebook_app_url_lazy():
    from django.conf import settings
    return '//apps.facebook.com/%s' % settings.FACEBOOK_APP_NAMESPACE
FACEBOOK_APP_URL = lazy(facebook_app_url_lazy, str)()
