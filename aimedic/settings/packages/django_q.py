Q_CLUSTER = {
    'name': 'aimedic',
    'workers': 8,
    'recycle': 500,
    "retry": 15,
    'timeout': 10,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'django_redis': 'default'
}
