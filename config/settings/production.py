from .base import *

# Override settings for production here
DEBUG = env.bool('DEBUG', default=False)

# Ensure ALLOWED_HOSTS is properly set in .env for production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '.onrender.com'])

# Render uses HTTPS by default, so we need to add the Render URL to CSRF_TRUSTED_ORIGINS
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_EXTERNAL_HOSTNAME}']

# Security Settings
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
