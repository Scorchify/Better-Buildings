from pathlib import Path
import dj_database_url
import os


#gps
if 'GDAL_LIBRARY_PATH' in os.environ:
    GDAL_LIBRARY_PATH = os.environ['GDAL_LIBRARY_PATH']

    
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['better-buildings-0b1289e952d7.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # My apps
    'better_buildings',
    'accounts',
    #google apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    #pwa configuration
    'pwa',

    # 3rd party
    'django_celery_beat',

    # Default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    #my middleware
    'better_buildings.middleware.getGeolocationMiddleware',
] 

ROOT_URLCONF = 'bb_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'better_buildings' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'better_buildings.context_processors.add_student_school',
                'better_buildings.context_processors.areas',
                'better_buildings.context_processors.supervisor_status',
                'better_buildings.context_processors.reports',
                'better_buildings.context_processors.announcements',
                'better_buildings.context_processors.unseen_announcements_count', 
            ],
            'libraries': {
                'custom_tags': 'better_buildings.templatetags.custom_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'bb_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',    #overwritten by postgresql
    },
}

DATABASES['default'] = dj_database_url.config(
    default=os.environ.get('DATABASE_URL'),
    conn_max_age=600,
    conn_health_checks=True,
)

DATABASE_ROUTERS = ['better_buildings.routers.SchoolDatabaseRouter']

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    BASE_DIR / 'better_buildings' / 'static',  # Adjusted to point to the static directory
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# My settings
LOGIN_REDIRECT_URL = 'better_buildings:index'
LOGOUT_REDIRECT_URL = 'better_buildings:index'
LOGIN_URL = 'login'
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  #standard django backend
    'accounts.backends.EmailOrUsernameModelBackend',  # Custom backend
    'allauth.account.auth_backends.AuthenticationBackend', # allauth backend
]

#Google Sign-In Settings
SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online"
        },
        'CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),  
        'SECRET': os.getenv('GOOGLE_CLIENT_SECRET'),  
    }
}
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True #Removes Intermediate Page for Google Sign-In
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.CustomSocialAccountAdapter'

#email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = 'password'

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'staticfiles', 'serviceworker.js')

#PWA Settings 
PWA_APP_NAME = 'Better-Buildings'
PWA_APP_DESCRIPTION = "Better Buildings, Ayden Yeung and Julian Givens (2024)"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/images/bb_logo.png',  # Updated to use the logo
        'sizes': '160x160'  # Adjust sizes as needed for your logo
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/images/bb_logo.png',  # Updated to use the logo
        'sizes': '160x160'  # Adjust sizes as needed for your logo
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/images/bb_logo.png',  # Updated to use the logo
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
