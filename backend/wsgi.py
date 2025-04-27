# College/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from College.scheduler import start_scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'College.settings')

application = get_wsgi_application()

# Start the scheduler
start_scheduler()
