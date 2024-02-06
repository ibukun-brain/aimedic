from aimedic.utils.settings import get_env_variable

AWS_QUERYSTRING_AUTH = False

AWS_DEFAULT_ACL = "public-read"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_LOCATION = "assets"

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
