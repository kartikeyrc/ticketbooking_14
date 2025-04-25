from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = 'django-insecure-h7l9y2#v9h2^7)%0u&!z#l+#a8s9t@5pm7=39b2xjh(k4-c@+n'
DEBUG = True  # Set to False when deploying to production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your domain here for deployment

# Add this line to fix the AutoField warning
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MySQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ticket_db',
        'USER': 'root',  # change to your MySQL username
        'PASSWORD': 'krc077@msql',  # change to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'booking',  # your custom app
]

# Make sure you also have these in your settings if not already:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ticket_booking_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # make sure you create this folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ticket_booking_system.wsgi.application'

# Static files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Authentication redirect (optional but helpful)
LOGIN_REDIRECT_URL = '/shows/'
LOGOUT_REDIRECT_URL = '/login/'

# Timezone and language
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


