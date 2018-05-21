from .base import *
ALLOWED_HOSTS = ['167.99.96.73','.appcocos.com']
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'cocosdb',
        'USER': 'postgres',
        'PASSWORD': '992424558',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
APPSECRET_PROOF = False