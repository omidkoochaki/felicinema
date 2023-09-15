from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p#h45&92z_r=#*$cnfnxkp8e&bi2qv$1ih%rb752#6fms^54qw'
ALLOWED_HOSTS = [
    'localhost',
]

CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "info.felicinema@gmail.com"
EMAIL_HOST_PASSWORD = "omgbgorzodjatzyb"