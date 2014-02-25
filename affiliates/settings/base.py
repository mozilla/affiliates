from funfactory.settings_base import *


# Django Settings
##############################################################################
ROOT_URLCONF = 'affiliates.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'affiliates.banners',
    'affiliates.base',
    'affiliates.facebook',
    'affiliates.links',
    'affiliates.users',

    'csp',
    'django_extensions',
    'django_statsd',
    'cronjobs',
    'jingo_minify',
    'mptt',
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
    'affiliates.base.middleware.PrivacyMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'affiliates.base.context_processors.common',
    'affiliates.base.context_processors.l10n',
    'affiliates.base.context_processors.month_year_picker',
    'affiliates.facebook.context_processors.app_context',
]

# Add Jingo loader
TEMPLATE_LOADERS = [
    'jingo.Loader',
] + list(TEMPLATE_LOADERS)

# Facebook auth middleware needs to come after AuthMiddleware but before
# session-csrf middleware so that it will generate csrf tokens.
auth_index = MIDDLEWARE_CLASSES.index('django.contrib.auth.middleware.AuthenticationMiddleware')
MIDDLEWARE_CLASSES.insert(auth_index + 1, 'affiliates.facebook.middleware.FacebookAuthenticationMiddleware')

# Language settings
PROD_LANGUAGES = ()

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

# Email settings
DEFAULT_FROM_EMAIL = 'notifications@affiliates.mozilla.org'

# Authentication
LOGIN_URL = '/'  # TODO: Change when we have a dedicated login view.
AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend', # required for admin
   'django_browserid.auth.BrowserIDBackend',
)

# Files
MAX_FILEPATH_LENGTH = 250

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Log out on browser close
SESSION_REMEMBER_DURATION = 1209600  # If we remember you, it lasts for 2 weeks

COOKIES_SECURE = True

# Set ALLOWED_HOSTS based on SITE_URL.
def _allowed_hosts():
    from django.conf import settings
    from urlparse import urlparse

    host = urlparse(settings.SITE_URL).netloc  # Remove protocol and path
    host = host.rsplit(':', 1)[0]  # Remove port
    return [host]
ALLOWED_HOSTS = lazy(_allowed_hosts, list)()

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


# Third-party Libary Settings
##############################################################################
# django-browserid Config
BROWSERID_DISABLE_SANITY_CHECKS = True
LOGIN_REDIRECT_URL = '/'

# Paths that do not need a locale
SUPPORTED_NONLOCALES += ['link', 'admin', 'browserid', 'fb']

# CacheMachine config
CACHE_COUNT_TIMEOUT = 60  # seconds, not too long.

# Email subscription config
BASKET_URL = 'http://basket.mozilla.com'
BASKET_NEWSLETTER = 'affiliates'

# Force session-csrf to give CSRF tokens to all users.
ANON_ALWAYS = True

# Template paths that should use django tempates instead of Jinja2.
JINGO_EXCLUDE_APPS = [
    'admin',
    'browserid',
    'smuggler',
    'fb',
    'registration',
]

# Activate statsd patches to time database and cache hits.
STATSD_PATCHES = [
    'django_statsd.patches.db',
    'django_statsd.patches.cache',
]

# CSP Config
CSP_EXCLUDE_URL_PREFIXES = ('/admin',)
CSP_SCRIPT_SRC = (
    '\'self\'',
    'https://*.mozilla.org',
    'http://*.mozilla.org',
    'https://*.mozilla.net',
    'http://*.mozilla.net',
    'http://login.persona.org',
    'https://login.persona.org',
    'http://*.google-analytics.com',
    'https://*.google-analytics.com',
)
CSP_FRAME_SRC = (
    '\'self\'',
    'https://login.persona.org'
)
CSP_IMG_SRC = (
    '\'self\'',
    'data:',
    'https://*.mozilla.org',
    'http://*.mozilla.org',
    'https://*.mozilla.net',
    'http://*.mozilla.net',
    'https://affiliates-cdn.mozilla.org',
    'https://secure.gravatar.com',
    'https://graph.facebook.com',
    'https://*.fbcdn.net',
    'https://*.akamaihd.net',
    'http://*.google-analytics.com',
    'https://*.google-analytics.com',
)
CSP_FONT_SRC = (
    '\'self\'',
    'https://*.mozilla.org',
    'http://*.mozilla.org',
    'https://*.mozilla.net',
    'http://*.mozilla.net',
)
CSP_STYLE_SRC = (
    '\'self\'',
    'https://*.mozilla.org',
    'http://*.mozilla.org',
    'https://*.mozilla.net',
    'http://*.mozilla.net',
)
CSP_OPTIONS = ('eval-script', 'inline-script')

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        # Mothership
        'base': (
            'css/base.styl',
            'browserid/persona-buttons.css',
        ),
        'oldIE': (
            'css/oldIE.styl',
            'browserid/persona-buttons.css',
        ),
        'home': (
            'css/home.styl',
        ),

        # Facebook app
        'fb_base': (
            'css/facebook.css',
            'css/month_year_picker.css',
        ),
    },
    'js': {
        # Mothership
        'base': (
            'js/libs/jquery-2.1.0.min.js',
            'browserid/browserid.js',
        ),
        'customize_image_banner': (
            'js/libs/rivets.min.js',
            'js/customize_image_banner.js',
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

# Use staticfiles loaders for finding resources for minification.
JINGO_MINIFY_USE_STATIC = True

# Default Nose arguments
NOSE_ARGS = ['--logging-filter=-django_browserid,-factory']


# Project-specific Settings
##############################################################################
# Locales that BrowserID is available in.
BROWSERID_LOCALES = [lang.lower() for lang in (
    'cs', 'de', 'en-US', 'es', 'fr', 'fy-NL', 'hr', 'nl', 'pl', 'pt-BR', 'sk',
    'sl', 'sq', 'sr', 'zh-TW')]

# List of valid country codes.
def lazy_countries():
    from product_details import product_details
    return product_details.get_regions('en-US')
COUNTRIES = lazy(lazy_countries, dict)()

# Paths for uploaded files.
def LOCALE_IMAGE_PATH(instance, filename):
    return 'uploads/locale_images/%s/%s' % (instance.locale, filename)
BANNER_IMAGE_PATH = 'uploads/banners/'

# Default image for badge previews to fall back on.
DEFAULT_BADGE_PREVIEW = MEDIA_URL + 'img/template/default-preview.png'

# CDN for absolutify.
CDN_DOMAIN = None

# URL to redirect to on affiliate link errors.
DEFAULT_AFFILIATE_LINK = 'http://mozilla.org'

# Leaderboard Display Size
LEADERBOARD_SIZE = 5

# Gravatar Settings
GRAVATAR_URL = 'https://secure.gravatar.com'
DEFAULT_GRAVATAR = MEDIA_URL + 'img/template/user-avatar.jpg'

# Bug 719522
# Old Firefox get redirected there
FIREFOX_UPGRADE_REDIRECT = 'http://www.mozilla.org/firefox/speed/?WT.mc_id=affaupgrade1&WT.mc_ev=click'

# Settings for Affiliates Facebook app
FACEBOOK_APP_NAMESPACE = 'affiliates'
FACEBOOK_PERMISSIONS = ''
FACEBOOK_LOCALES = ('en-us', 'de', 'es', 'fr', 'nl', 'pl', 'pt-br', 'sq', 'zh-tw')
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

# Google Analytics
GA_ACCOUNT_CODE = ''
