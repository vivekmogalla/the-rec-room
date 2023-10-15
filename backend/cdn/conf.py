import os
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
     "ACL": "public-read"
}
AWS_LOCATION = "https://djangostoragew.blr1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE = "djangostoragew.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE = 'djangostoragew.cdn.backends.StaticRootS3BotoStorage'