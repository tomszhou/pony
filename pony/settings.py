"""
Django settings for stride project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p*ggd=o#y8ws1fmpup!jnw9m0mo=4+fs1a!l!eu%h&b=jfx$x#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "10.0.138.237",
    "blog.localhost.com",
]

# LOAD INI CONFIG
DEV_INI_PATH = os.path.join(BASE_DIR, 'config/develop')
PRO_INI_PATH = os.path.join(BASE_DIR, 'config/product')
INI_PATH = DEV_INI_PATH if DEBUG else PRO_INI_PATH

# APP通用配置
INI_CONFIG = configparser.ConfigParser()
INI_CONFIG.read(os.path.join(INI_PATH, 'config.ini'))

# Memcached配置
INI_MEMCACHED = configparser.ConfigParser()
INI_MEMCACHED.read(os.path.join(INI_PATH, 'memcache.ini'))

# Mysql配置
INI_MYSQL = configparser.ConfigParser()
INI_MYSQL.read(os.path.join(INI_PATH, 'mysql.ini'))

# RabbitMQ配置
INI_RABBIT = configparser.ConfigParser()
INI_RABBIT.read(os.path.join(INI_PATH, 'rabbit.ini'))

# Redis配置
INI_REDIS = configparser.ConfigParser()
INI_REDIS.read(os.path.join(INI_PATH, 'redis.ini'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义授权帮助中间件
    'app.middleware.auth.AuthMiddleware',
]

ROOT_URLCONF = 'pony.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'pony.wsgi.application'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    # 日志格式
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s \
            [%(levelname)s- %(message)s]]",
        }
    },
    # 过滤器
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    # 处理器
    "handlers": {
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/data/wwwlogs/pony_error.log",
            "maxBytes": 1024*1024*5,
            "backupCount": 5,
            "formatter": "standard",
        }
    },
    # logging管理器
    "loggers": {
        "pony": {
            "handlers": ["error"],
            "level": "ERROR",
            "propagate": True,
        }
    }
}

# Session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = dict()
for section in INI_MYSQL.sections():
    item = dict()
    item["ENGINE"] = "django.db.backends.mysql"
    item["NAME"] = 'b_django' if section == 'default' else section
    item["HOST"] = INI_MYSQL[section]["master.host"]
    item["USER"] = INI_MYSQL[section]["master.username"]
    item["PASSWORD"] = INI_MYSQL[section]["master.password"]
    DATABASES = dict(DATABASES, **{section: item})

DATABASE_ROUTERS = ["pony.db_router.DBRouter"]
DATABASE_MAPPING = {
    "b_account": "b_account",
    "b_blog": "b_blog",
}


# Cache
# 缓存配置，默认使用Memcached
MEMCACHED_LOCATIONS = []
for section in INI_MEMCACHED.sections():
    section = INI_MEMCACHED[section]
    ip_address = section["host"]+":"+section["port"]
    MEMCACHED_LOCATIONS.append(ip_address)


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': MEMCACHED_LOCATIONS
    }
}


REDIS = {
    "host": INI_REDIS["redis"]["redis.host"],
    "port": INI_REDIS["redis"]["redis.port"],
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# 上传图片路径
IMAGE_HOST = INI_CONFIG["upload"]["app.imageUri"]
UPLOAD_IMAGE_PATH = INI_CONFIG["upload"]["app.imageUploadPath"]


# 上传视频路径
VIDEO_HOST = INI_CONFIG["upload"]["app.videoUri"]
UPLOAD_VIDEO_PATH = INI_CONFIG["upload"]["app.videoUploadPath"]

