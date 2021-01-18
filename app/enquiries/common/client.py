import logging
from urllib.parse import urljoin, urlparse

import requests
from requests.exceptions import ConnectionError
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class BadGatewayAPIException(APIException):
    """DRF Exception for the 502 status code."""

    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Bad Gateway."
    default_code = "bad_gateway"


class APIClient:
    """Generic API Client."""
    DEFAULT_ACCEPT = "application/json;q=0.9,*/*;q=0.8"

    def __init__(
        self,
        api_url,
        auth=None,
        accept=DEFAULT_ACCEPT,
        default_timeout=None,
        raise_for_status=True,
        request=None,
    ):
        """Initialises the API client."""
        self._api_url = api_url
        self._auth = auth
        self._accept = accept
        self._default_timeout = default_timeout
        self._raise_for_status = raise_for_status
        self._request = request

    def request(self, method, path, **kwargs):
        """Makes an HTTP request."""
        url = urljoin(self._api_url, path)
        logger.info(f"Sending request: {method.upper()} {url}")

        timeout = kwargs.pop("timeout", self._default_timeout)

        headers = kwargs.pop("headers", {})
        if self._accept:
            headers["Accept"] = self._accept

        try:
            response = requests.request(
                method,
                url,
                auth=self._auth,
                headers=headers,
                timeout=timeout,
                **kwargs,
            )
        except ConnectionError as e:
            logger.exception(e)
            raise BadGatewayAPIException(
                f"Upstream service unavailable: {urlparse(url).netloc}",
            ) from e
        logger.info(f"Response received: {response.status_code} {method.upper()} {url}")
        if self._raise_for_status:
            response.raise_for_status()
        return response
