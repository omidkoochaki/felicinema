import os

SECRET_KEY = os.getenv('SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "info.felicinema@gmail.com"
EMAIL_HOST_PASSWORD = "omgbgorzodjatzyb"