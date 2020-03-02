from django.conf import settings

def get_oauth_payload(request):
    return request.session.get(settings.AUTHBROKER_TOKEN_SESSION_KEY)
