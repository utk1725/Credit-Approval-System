import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval.settings')
app = Celery('credit_approval')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
