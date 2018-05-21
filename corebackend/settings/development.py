from .base import *
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'cocosdb',
        'USER': 'richardcancino',
        'PASSWORD': '992424558',
        'HOST': 'localhost',
        'PORT': '',
    }
}