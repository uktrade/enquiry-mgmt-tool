import datetime
from collections.abc import Mapping, Sequence

import mohawk
import pytest
from django.urls import reverse, path
from freezegun import freeze_time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from app.enquiries import auth
from app.enquiries.tests.factories import OwnerFactory

HAWK_CREDENTIALS = {
    "test-id-without-scope": {
        "key": "test-key-without-scope",
        "scopes": (),
    },
    "test-id-with-scope": {
        "key": "test-key-with-scope",
        "scopes": ("enquiries",),
    },
    "test-id-with-multiple-scopes": {
        "key": "test-key-with-multiple-scopes",
        "scopes": ("enquiries", "views"),
    },
}


class HawkViewWithoutScope(auth.HawkResponseSigningMixin, APIView):
    """View using Hawk authentication."""

    authentication_classes = (auth.HawkAuthentication,)
    permission_classes = ()

    def get(self, request):
        """Simple test view with fixed response."""
        return Response({"content": "hawk-test-view-without-scope"})


class HawkViewWithScope(auth.HawkResponseSigningMixin, APIView):
    """View using Hawk authentication."""

    authentication_classes = (auth.HawkAuthentication,)
    permission_classes = (auth.HawkScopePermission,)
    required_hawk_scope = "enquiries"

    def get(self, request):
        """Simple test view with fixed response."""
        return Response({"content": "hawk-test-view-with-scope"})


class PaasIPView(APIView):
    """View using PaaS IP Authentication."""

    authentication_classes = (auth.PaaSIPAuthentication,)
    permission_classes = ()

    def get(self, request):
        """Simple test view with fixed response."""
        return Response({"content": "paas-ip-test-view"})


urlpatterns = [
    path(
        "test-hawk-without-scope/",
        HawkViewWithoutScope.as_view(),
        name="test-hawk-without-scope",
    ),
    path(
        "test-hawk-with-scope/",
        HawkViewWithScope.as_view(),
        name="test-hawk-with-scope",
    ),
    path(
        "test-paas-ip/",
        PaasIPView.as_view(),
        name="test-paas-ip",
    ),
]


def _url():
    return "http://testserver" + reverse("test-hawk-without-scope")


def _url_incorrect_domain():
    return "http://incorrect" + reverse("test-hawk-without-scope")


def _url_incorrect_path():
    return "http://testserver" + reverse("test-hawk-without-scope") + "incorrect/"


def _url_with_scope():
    return "http://testserver" + reverse("test-hawk-with-scope")


def _auth_sender(
    key_id="test-id-without-scope",
    secret_key="test-key-without-scope",
    url=_url,
    method="GET",
    content="",
    content_type="",
):
    credentials = {
        "id": key_id,
        "key": secret_key,
        "algorithm": "sha256",
    }
    return mohawk.Sender(
        credentials,
        url(),
        method,
        content=content,
        content_type=content_type,
    )


def identity(value):
    """Pass through a single argument unchanged."""
    return value


def resolve_data(data, value_resolver=identity):
    """
    Recursively resolve callables in data structures.

    Given a value:

    - if it's a callable, resolve it
    - if it's a sequence, resolve each of the sequence's values
    - if it's a dict, resolve each value of the dict

    The resolved value is returned.

    Used in parametrised tests.
    """
    if isinstance(data, Mapping):
        return {
            key: resolve_data(value, value_resolver=value_resolver)
            for key, value in data.items()
        }

    if isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
        return [resolve_data(value, value_resolver=value_resolver) for value in data]

    if callable(data):
        return value_resolver(data())

    return value_resolver(data)


@pytest.mark.django_db
@pytest.mark.urls("app.enquiries.tests.test_auth")
class TestHawkAuthentication:
    """Tests Hawk authentication when using HawkAuthentication."""

    @pytest.mark.parametrize(
        "get_kwargs,expected_json",
        (
            (
                # If the Authorization header isn't passed
                {
                    "content_type": "",
                },
                {"detail": "Authentication credentials were not provided."},
            ),
            (
                # If the Authorization header generated from an incorrect ID
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION": lambda: _auth_sender(key_id="incorrect").request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
            (
                # If the Authorization header generated from an incorrect secret
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION":
                        lambda: _auth_sender(secret_key="incorrect").request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
            (
                # If the Authorization header generated from an incorrect domain
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION":
                        lambda: _auth_sender(url=_url_incorrect_domain).request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
            (
                # If the Authorization header generated from an incorrect path
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION":
                        lambda: _auth_sender(url=_url_incorrect_path).request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
            (
                # If the Authorization header generated from an incorrect method
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION": lambda: _auth_sender(method="POST").request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
            (
                # If the Authorization header generated from an incorrect
                # content-type
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION":
                        lambda: _auth_sender(content_type="incorrect").request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
            (
                # If the Authorization header generated from incorrect content
                {
                    "content_type": "",
                    "HTTP_AUTHORIZATION": lambda: _auth_sender(content="incorrect").request_header,
                },
                {"detail": "Incorrect authentication credentials."},
            ),
        ),
    )
    def test_401_returned(self, api_client, get_kwargs, expected_json):
        """If the request isn't properly Hawk-authenticated, then a 401 is
        returned
        """
        resolved_get_kwargs = resolve_data(get_kwargs)
        response = api_client.get(
            _url(),
            **resolved_get_kwargs,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == expected_json

    def test_if_61_seconds_in_past_401_returned(self, api_client):
        """If the Authorization header is generated 61 seconds in the past, then a
        401 is returned
        """
        past = datetime.datetime.now() - datetime.timedelta(seconds=61)
        with freeze_time(past):
            auth = _auth_sender().request_header
        response = api_client.get(
            reverse("test-hawk-without-scope"),
            content_type="",
            HTTP_AUTHORIZATION=auth,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Incorrect authentication credentials."}

    @pytest.mark.usefixtures("local_memory_cache")
    def test_if_authentication_reused_401_returned(self, api_client, settings):
        """If the Authorization header is reused, then a 401 is returned"""
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        auth = _auth_sender().request_header
        response_1 = api_client.get(
            _url(),
            content_type="",
            HTTP_AUTHORIZATION=auth,
        )
        assert response_1.status_code == status.HTTP_200_OK

        response_2 = api_client.get(
            _url(),
            content_type="",
            HTTP_AUTHORIZATION=auth,
        )
        assert response_2.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_2.json() == {"detail": "Incorrect authentication credentials."}

    def test_returned_object_with_authentication_3_ips(self, api_client, settings):
        """If the Authorization and X-Forwarded-For headers are correct,
        with an extra IP address prepended to the X-Forwarded-For then
        the correct, and authentic, data is returned
        """
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        sender = _auth_sender()
        response = api_client.get(
            _url(),
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"content": "hawk-test-view-without-scope"}

    def test_returned_object_with_authentication(self, api_client, settings):
        """If the Authorization and X-Forwarded-For headers are correct, then
        the correct, and authentic, data is returned
        """
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        sender = _auth_sender()
        response = api_client.get(
            _url(),
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"content": "hawk-test-view-without-scope"}


@pytest.mark.django_db
@pytest.mark.urls("app.enquiries.tests.test_auth")
class TestHawkResponseSigningMixin:
    """Tests Hawk response signing when using HawkResponseMiddleware."""

    def test_returned_object_with_authentication(self, api_client, settings):
        """If the Authorization and X-Forwarded-For headers are correct, then
        the correct, and authentic, data is returned
        """
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        sender = _auth_sender()
        response = api_client.get(
            _url(),
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
        )

        assert response.status_code == status.HTTP_200_OK

        # Just asserting that accept_response doesn't raise is a bit weak,
        # so we also assert that it raises if the header, content, or
        # content_type are incorrect
        sender.accept_response(
            response_header=response["Server-Authorization"],
            content=response.content,
            content_type=response["Content-Type"],
        )
        with pytest.raises(mohawk.exc.MacMismatch):
            sender.accept_response(
                response_header='Hawk mac="incorrect", hash="incorrect"',
                content=response.content,
                content_type=response["Content-Type"],
            )
            with pytest.raises(mohawk.exc.MisComputedContentHash):
                sender.accept_response(
                    response_header=response["Server-Authorization"],
                    content="incorrect",
                    content_type=response["Content-Type"],
                )
            with pytest.raises(mohawk.exc.MisComputedContentHash):
                sender.accept_response(
                    response_header=response["Server-Authorization"],
                    content=response.content,
                    content_type="incorrect",
                )

    def test_does_not_sign_non_hawk_requests(self):
        """Test that a 403 is returned if the request is not authenticated using Hawk."""
        from rest_framework.test import force_authenticate

        factory = APIRequestFactory()
        user = OwnerFactory()
        view = HawkViewWithScope.as_view()

        request = factory.get("/test-hawk-with-scope/")
        force_authenticate(request, user=user)
        response = view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": "You do not have permission to perform this action.",
        }


@pytest.mark.django_db
@pytest.mark.urls("app.enquiries.tests.test_auth")
class TestHawkScopePermission:
    """Tests scoped-based permissions using HawkScopePermission."""

    def test_denies_access_when_without_the_required_scope(self, api_client, settings):
        """
        Test that a 403 is returned if the request is Hawk authenticated but the client doesn't
        have the required scope.
        """
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        sender = _auth_sender(
            key_id="test-id-without-scope",
            secret_key="test-key-without-scope",
            url=_url_with_scope,
        )
        response = api_client.get(
            _url_with_scope(),
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {
            "detail": "You do not have permission to perform this action.",
        }

    def test_denies_access_if_not_authenticated_using_hawk(self):
        """Test that a 403 is returned if the request is not authenticated using Hawk."""
        from rest_framework.test import force_authenticate

        factory = APIRequestFactory()
        user = OwnerFactory()
        view = HawkViewWithScope.as_view()

        request = factory.get("/test-hawk-with-scope/")
        force_authenticate(request, user=user)
        response = view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": "You do not have permission to perform this action.",
        }

    def test_authorises_when_with_the_required_scope(self, api_client, settings):
        """
        Test that a 200 is returned if the request is Hawk authenticated and the client has
        the required scope.
        """
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        sender = _auth_sender(
            key_id="test-id-with-scope",
            secret_key="test-key-with-scope",
            url=_url_with_scope,
        )
        response = api_client.get(
            _url_with_scope(),
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"content": "hawk-test-view-with-scope"}

    def test_authorises_when_with_one_of_the_required_scopes(self, api_client, settings):
        """
        Test that a 200 is returned if the request is Hawk authenticated and the client has
        one of the required scope.
        """
        settings.HAWK_CREDENTIALS = HAWK_CREDENTIALS
        sender = _auth_sender(
            key_id="test-id-with-multiple-scopes",
            secret_key="test-key-with-multiple-scopes",
            url=_url_with_scope,
        )
        response = api_client.get(
            _url_with_scope(),
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"content": "hawk-test-view-with-scope"}
