from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3BotoStorage(S3Boto3Storage):
    location = "staticfiles"
    file_overwrite = False


class MediaRootS3BotoStorage(S3Boto3Storage):
    location = 'mediafiles'
    file_overwrite = False