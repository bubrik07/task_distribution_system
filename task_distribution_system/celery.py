from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_distribution_system.settings')

app = Celery(
    'task_distribution_system',
    broker='redis://localhost:6379/0',
)

app.conf.update(
    result_backend='redis://localhost:6379/0',  # For saving results
    accept_content=['json'],                    # Only JSON
    task_serializer='json',                     # Task serializer format
    timezone='UTC',                             # Timezone
    result_extended=True,                       # More info in results
    beat_schedule={  # Schedule for periodic tasks
        'distribute-tasks-every-30-seconds': {
            'task': 'your_app_name.tasks.distribute_tasks',  # Шлях до твоєї задачі
            'schedule': 30.0,  # Запуск кожні 10 секунд
        },
    },
)

logger.info(f"Broker URL: {app.conf.broker_url}")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
