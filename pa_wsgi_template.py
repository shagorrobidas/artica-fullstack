import os
import sys

# Add your project directory to the sys.path
path = '/home/shagorrobidasjvai/artica-fullstack'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

# Activate your virtualenv (optional but recommended)
# Note: You should specify your actual virtualenv path here if using one
# activate_this = '/home/<your-username>/.virtualenvs/myenv/bin/activate_this.py'
# with open(activate_this) as f:
#     exec(f.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
