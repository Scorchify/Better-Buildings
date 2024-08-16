from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c^x4r3&xt3_3)7r_ja&!g*^brcun)blx+x_9hg^+wb1z6n6#@b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
    'allauth.socialaccount.providers.google',  # Google provider

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'better_buildings.middleware.getIPAddressMw',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'bb_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'better_buildings' / 'templates'],  # Adjusted to point to the templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # my context processors
                'better_buildings.context_processors.add_student_school', 
                'better_buildings.context_processors.areas', 
                'better_buildings.context_processors.supervisor_status', 
            ],
        },
    },
]

WSGI_APPLICATION = 'bb_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

   'WheatonHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'Wheaton.sqlite3',
    },
    
    'MBlairHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'MBlairHS.sqlite3',
    },

    'AEinsteinHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'AEinsteinHS.sqlite3',
    },

    'JFKHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'JFKHS.sqlite3',
    },

    'NorthwoodHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'NorthwoodHS.sqlite3',
    },

     'WhitmanHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WhitmanHS.sqlite3',
    },
    
     'PoolesvilleHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'PoolesvilleHS.sqlite3',
    },

     'WoottonHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WoottonHS.sqlite3',
    },

     'ChurchillHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ChurchillHS.sqlite3',
    },

     'RMontgomeryHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RMontgomeryHS.sqlite3',
    },

     'BCCHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'BCCHS.sqlite3',
    },

     'WJohnsonHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WJohnsonHS.sqlite3',
    },

     'NorthwestHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'Northwest.sqlite3',
    },

     'ClarksburgHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ClarksburgHS.sqlite3',
    },

     'SpringbrookHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SpringbrookHS.sqlite3',
    },

     'SherwoodHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SherwoodHS.sqlite3',
    },

    'DamascusHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'DamascusHS.sqlite3',
    },

    'MagruderHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'MagruderHS.sqlite3',
    },

    'RockvilleHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RockvilleHS.sqlite3',
    },

    'PaintBranchHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'PaintBranchHS.sqlite3',
    },
    
    'QuinceOrchardHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'QuinceOrchardHS.sqlite3',
    },

    'BlakeHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'BlakeHS.sqlite3',
    },

    'SenecaHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SenecaHS.sqlite3',
    },

    'GaithersburgHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'GaithersburgHS.sqlite3',
    },

    'WatkinsMillHS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WatkinsMillHS.sqlite3',
    },
    #middle schools
    'ArgyleMS': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'ArgyleMS.sqlite3',
    },

    'JohnTBakerMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'JohnTBakerMS.sqlite3',
    },

    'BenjaminBannekerMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'BenjaminBannekerMS.sqlite3',
    },

    'BriggsChaneyMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'BriggsChaneyMS.sqlite3',
    },
    
    'CabinJohnMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'CabinJohnMS.sqlite3',
    },

    'RobertoWClementeMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RobertoWClementeMS.sqlite3',
    },

    'EasternMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'EasternMS.sqlite3',
    },

    'WilliamHFarquharMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WilliamHFarquharMS.sqlite3',
    },

    'ForestOakMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ForestOakMS.sqlite3',
    },

    'RobertFrostMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RobertFrostMS.sqlite3',
    },

    'GaithersburgMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'GaithersburgMS.sqlite3',
    },

    'HerbertHooverMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'HerbertHooverMS.sqlite3',
    },

    'FrancisScottKeyMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'FrancisScottKeyMS.sqlite3',
    },

    'DrMartinLutherKingJrMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'DrMartinLutherKingJrMS.sqlite3',
    },

    'KingsviewMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'KingsviewMS.sqlite3',
    },

    'LakelandsParkMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'LakelandsParkMS.sqlite3',
    },

    'AMarioLoiedermanMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'AMarioLoiedermanMS.sqlite3',
    },

    'MontgomeryVillageMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'MontgomeryVillageMS.sqlite3',
    },

    'NeelsvilleMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'NeelsvilleMS.sqlite3',
    },

    'NewportMillMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'NewportMillMS.sqlite3',
    },

    'NorthBethesdaMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'NorthBethesdaMS.sqlite3',
    },

    'ParklandMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ParklandMS.sqlite3',
    },

    'RosaMParksMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RosaMParksMS.sqlite3',
    },

    'JohnPooleMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'JohnPooleMS.sqlite3',
    },
    'ThomasWPyleMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ThomasWPyleMS.sqlite3',
    },

    'RedlandMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RedlandMS.sqlite3',
    },

    'RidgeviewMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RidgeviewMS.sqlite3',
    },

    'RockyHillMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'RockyHillMS.sqlite3',
    },

    'ShadyGroveMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'ShadyGroveMS.sqlite3',
    },

    'OdessaShannonMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'OdessaShannonMS.sqlite3',
    },
    
    'SilverCreekMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SilverCreekMS.sqlite3',
    },

    'SilverSpringIntlMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SilverSpringIntlMS.sqlite3',
    },

    'SligoMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SligoMS.sqlite3',
    },

    'TakomaParkMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'TakomaParkMS.sqlite3',
    },

    'TildenMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'TildenMS.sqlite3',
    },

    'HallieWellsMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'HallieWellsMS.sqlite3',
    },

    'JuliusWestMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'JuliusWestMS.sqlite3',
    },

    'WestlandMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WestlandMS.sqlite3',
    },

    'WhiteOakMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'WhiteOakMS.sqlite3',
    },
    
    'EarleBWoodMS': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'EarleBWoodMS.sqlite3',
    },
}

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

STATIC_URL = 'static/'
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
        }
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
EMAIL_HOST_USER = '171524@mcpsmd.net'
EMAIL_HOST_PASSWORD = 'password'