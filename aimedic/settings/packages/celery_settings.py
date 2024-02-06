from aimedic.utils.settings import get_env_variable

CELERY_RESULT_BACKEND = get_env_variable("REDIS_URL", "redis://localhost:6379/0")

BROKER_URL = CELERY_RESULT_BACKEND

CELERY_BROKER_URL = CELERY_RESULT_BACKEND

CELERY_ACCEPT_CONTENT = ["application/json"]

CELERY_TASK_SERIALIZER = "json"

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [get_env_variable('REDIS_URL',("127.0.0.1", 6379))],
#         },
#     },
# }
