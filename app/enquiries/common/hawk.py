import logging

from mohawk import Sender
from requests.auth import AuthBase

logger = logging.getLogger(__name__)


class HawkAuth(AuthBase):
    """Hawk authentication class."""

    def __init__(self, api_id, api_key, signing_algorithm="sha256", verify_response=True):
        """Initialises the authenticator with the signing parameters."""
        self._api_id = api_id
        self._api_key = api_key
        self._signing_algorithm = signing_algorithm
        self._verify_response = verify_response

    def __call__(self, request):
        """Signs a request, and attaches a response verifier."""
        credentials = {
            "id": self._api_id,
            "key": self._api_key,
            "algorithm": self._signing_algorithm,
        }

        sender = Sender(
            credentials,
            request.url,
            request.method,
            content=request.body or "",
            content_type=request.headers.get("Content-Type", ""),
        )

        request.headers["Authorization"] = sender.request_header
        if self._verify_response:
            request.register_hook("response", make_response_verifier(sender))

        return request


def make_response_verifier(sender):
    def verify_response(response, *args, **kwargs):
        if response.ok:
            sender.accept_response(
                response.headers["Server-Authorization"],
                content=response.content,
                content_type=response.headers["Content-Type"],
            )

    return verify_response
