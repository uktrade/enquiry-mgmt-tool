from app.settings.common import *

ROOT_URLCONF = 'app.testfixtureapi_urls'

# For local/E2E tests use "plain" logging (read non ASIM formatted)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] [%(levelname)-4s] %(name)-8s: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG' if env.bool('DEBUG') else 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
}