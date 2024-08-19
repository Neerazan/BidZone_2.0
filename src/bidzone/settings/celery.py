from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_BEAT_SCHEDULE = {
    # 'notify_customers': {
    #     'task': 'playground.tasks.notify_customers',
    #     'schedule': 5,
    #     'args': ['Hello World'],
    # }
    'process-completed-auctions': {
        'task': 'auction.tasks.process_completed_auctions',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}
