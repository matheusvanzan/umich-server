# ######### VARIABLES FOR THIS PROJECT
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ######### DEBUG
DEBUG = True  # Django default split, real deBugging
TEMPLATE_DEBUG = DEBUG
MY_DEBUG = False  # To split development/production files

########## ADMIN
ADMINS = (
    ('Matheus Vanzan', 'vanzan2015@gmail.com'),
    ('Marcos Valle', 'marcosvalle01@gmail.com'),
)
MANAGERS = ADMINS

########## PROJECT SPECIFIC
if MY_DEBUG:
    PROJECT = 'server'
    REAL_PROJECT = PROJECT
    APPS = ('myproject', )
else:
    PROJECT = 'myproject'
    REAL_PROJECT = 'server'
    APPS = ('myproject', )

if MY_DEBUG:
    MY_DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'server',
            'USER': 'vanzan',
            'PASSWORD': 'vanzan',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }
else:
    MY_DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'server',
            'USER': 'vanzan',
            'PASSWORD': 'vanzan',
            'HOST': 'web443.webfaction.com',
            'PORT': '',
        }
    }


########## COMMON SETTINGS
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)
INSTALLED_APPS = INSTALLED_APPS, APPS
INSTALLED_APPS = INSTALLED_APPS[0] + INSTALLED_APPS[1]

SECRET_KEY = '^io4ungjk+1v+@tm655ks2)#*o8*w2mig1nhhk(u4fe36kjc-6'

SITE_ID = 1

ROOT_URLCONF = PROJECT + '.urls'
WSGI_APPLICATION = PROJECT + '.wsgi.application'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

########## DEVELOPMENT/PRODUCTION SETTTINGS
if MY_DEBUG:
    ########## DEVELOPMENT SETTINGS
    DATABASES = MY_DATABASES


    ########## STATIC AND TEMPLATES
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        #'django.template.loaders.eggs.Loader',
    )

    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )

    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
else:
    ########## PRODUCTION SETTINGS
    DATABASES = MY_DATABASES

    ########## STATIC AND TEMPLATES
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    SITE_NAME = str(BASE_DIR).split('/')[-2]

    ALLOWED_HOSTS = ['vanzan2015.webfactional.com']

    # Where files are stored inside the server
    STATIC_URL = '/static/' + REAL_PROJECT + '/'
    STATIC_ROOT = '/home/vanzan2015/webapps/static/' + REAL_PROJECT

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, '../../' + REAL_PROJECT + '/myproject/myproject/static'),
    )

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, '../../' + REAL_PROJECT + '/myproject/myproject/templates'),
    )
