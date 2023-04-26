from pathlib import Path
import os
import environ
from decouple import config
from dj_database_url import parse as dburl

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = 'django-insecure-h(gd%^y(9$#nn%&kau3@9h-0-n!t%)3ly944$9vva4x!y@7roe'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 追加
    'django.contrib.sites', # 追加
    'allauth', # 追加
    'allauth.account', # 追加
    'allauth.socialaccount', # 追加
    'allauth.socialaccount.providers.google', # 追加
    'accounts' # 追加
    #'user_profile',
    #'main'
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
]

ROOT_URLCONF = 'PetMatch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # templatesディレクトリを設定
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

WSGI_APPLICATION = 'PetMatch.wsgi.application'

default_dburl = "sqlite:///" + str(BASE_DIR / "db.sqlite3")
DATABASES = {
    'default': config("DATABASE_URL", default=default_dburl, cast=dburl)
}



LOGIN_REDIRECT_URL = "accounts:index"
LOGOUT_REDIRECT_URL = "accounts:login"
AUTH_USER_MODEL = "accounts.User" # カスタムユーザーを認証用ユーザーとして登録

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

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = 'static/'
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '284665082017-7ksi08drumltj8uginb1t9ue9kuo05lc.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'accounts.pipeline.create_user_by_google',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


SUPERUSER_NAME = env("SUPERUSER_NAME") 
SUPERUSER_EMAIL = env("SUPERUSER_EMAIL")
SUPERUSER_PASSWORD = env("SUPERUSER_PASSWORD")