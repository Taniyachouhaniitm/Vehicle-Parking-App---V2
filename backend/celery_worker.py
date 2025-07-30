from celery_app import celery

celery.autodiscover_tasks(['tasks'])