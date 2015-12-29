# custom_storages.py
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
	ocation = settings.STATICFILES_LOCATION

class MediaStorage(S3BotoStorage):
	location = settings.MEDIAFILES_LOCATION