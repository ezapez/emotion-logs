from django.conf import settings


def google_oauth(request):
    return {'google_oauth_enabled': settings.GOOGLE_OAUTH_ENABLED}
