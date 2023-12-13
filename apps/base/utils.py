from django.urls import reverse
from django.conf import settings


def get_frontend_url(url_name, *args):
    frontend_domain = getattr(settings, 'FRONTEND_DOMAIN', None)
    if frontend_domain is None:
        raise ValueError('FRONTEND_DOMAIN is not configured in settings')
    url = reverse(url_name, args=[*args])
    frontend_url = frontend_domain + url
    return frontend_url
