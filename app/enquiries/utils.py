from django.conf import settings

def get_oauth_payload(request):
    """
    Returns the Staff SSO oauth data stored in the session (i.e. oauth token, expiry time etc )
    (the oauth data is need for authentication with data and other services authenticated via Staff SSO)
    """
    return request.session.get(settings.AUTHBROKER_TOKEN_SESSION_KEY, None)
