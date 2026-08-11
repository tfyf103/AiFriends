"""Central refresh-cookie policy.

Keeping cookie options in one helper prevents login/register/refresh from drifting apart.
Development uses HTTP, so ``secure`` is false while DEBUG is true; production should
serve HTTPS and therefore gets a secure cookie automatically.
"""

from django.conf import settings


REFRESH_COOKIE_NAME = 'refresh_token'
REFRESH_COOKIE_MAX_AGE = 60 * 60 * 24 * 7


def set_refresh_cookie(response, token):
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=str(token),
        httponly=True,
        samesite='Lax',
        secure=not settings.DEBUG,
        max_age=REFRESH_COOKIE_MAX_AGE,
        path='/',
    )
    return response


def delete_refresh_cookie(response):
    response.delete_cookie(
        REFRESH_COOKIE_NAME,
        path='/',
        samesite='Lax',
    )
    return response
