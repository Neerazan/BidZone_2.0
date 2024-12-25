# gunicorn_config.py
import multiprocessing
import os

# Path configuration
base_dir = os.path.dirname(os.path.abspath(__file__))
pythonpath = os.path.join(base_dir, 'src')

# Server socket
bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1

# Logging
accesslog = os.path.join(base_dir, 'logs/access.log')
errorlog = os.path.join(base_dir, 'logs/error.log')
loglevel = 'info'
capture_output = True

# Reload & Environment
reload = False
raw_env = ['DJANGO_SETTINGS_MODULE=bidzone.settings']

# Timeouts
timeout = 120
graceful_timeout = 30
