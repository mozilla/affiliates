# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Logging
SYSLOG_TAG = "http_app_playdoh"  # Make this unique to your project.


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
    }
}

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'affiliates',
    'users',
]

# Email settings
DEFAULT_FROM_EMAIL = 'notifications@affiliates.mozilla.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACTIVATION_EMAIL = 'users/email/activation.ltxt'

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
