import pytest
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from app.enquiries.common.client import APIClient, BadGatewayAPIException

BASE = "http://local.host/"


class TestAPIClient:
    """Tests APIClient."""

    def test_successful_request(self, requests_mock):
        """Tests making a successful request."""
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=200)

        api_client = APIClient(api_url)
        response = api_client.request("GET", "path/to/item")

        assert response.status_code == 200
        assert response.request.headers["Accept"] == APIClient.DEFAULT_ACCEPT
        assert response.request.timeout is None

    def test_request_error(self):
        """
        Tests that a BadGatewayAPIException exception is raised on connection error.
        """
        api_url = f"{BASE}v1/"
        api_client = APIClient(api_url, raise_for_status=True)
        with pytest.raises(BadGatewayAPIException) as e:
            api_client.request("GET", "path/to/item")
        assert "Upstream service unavailable: local.host" in str(e)

    def test_raises_exception_on_unsuccessful_request_if_flag_is_true(self, requests_mock):
        """
        Tests that an exception is raised on an successful request
        if the raise_for_status argument is True.
        """
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=404)

        api_client = APIClient(api_url, raise_for_status=True)
        with pytest.raises(HTTPError) as excinfo:
            api_client.request("GET", "path/to/item")

        assert excinfo.value.response.status_code == 404

    def test_doesnt_raise_exception_on_unsuccessful_request_if_flag_is_false(self, requests_mock):
        """
        Tests that no exception is raised on an successful request
        if the raise_for_status argument is False.
        """
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=404)

        api_client = APIClient(api_url, raise_for_status=False)
        response = api_client.request("GET", "path/to/item")

        assert response.status_code == 404

    def test_passes_through_arguments(self, requests_mock):
        """Tests that auth, accept and default_timeout are passed to the request."""
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=200)

        api_client = APIClient(
            api_url,
            auth=HTTPBasicAuth("user", "password"),
            accept="test-accept",
            default_timeout=10,
        )
        response = api_client.request("GET", "path/to/item")

        assert response.status_code == 200
        assert response.request.headers["Accept"] == "test-accept"
        assert response.request.timeout == 10

    def test_omits_accept_if_none(self, requests_mock):
        """Tests that the Accept header is not overridden when accept=None is passed."""
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=200)

        api_client = APIClient(
            api_url,
            auth=HTTPBasicAuth("user", "password"),
            accept=None,
        )
        response = api_client.request("GET", "path/to/item")

        assert response.status_code == 200
        assert response.request.headers["Accept"] == "*/*"

    @pytest.mark.parametrize("default_timeout", (10, None))
    def test_can_override_timeout_per_request(self, requests_mock, default_timeout):
        """Tests that the timeout can be overridden for a specific request."""
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=200)

        api_client = APIClient(
            api_url,
            auth=HTTPBasicAuth("user", "password"),
            accept="test-accept",
            default_timeout=default_timeout,
        )
        response = api_client.request("GET", "path/to/item", timeout=20)

        assert response.status_code == 200
        assert response.request.headers["Accept"] == "test-accept"
        assert response.request.timeout == 20

    def test_can_specify_headers(self, requests_mock):
        """Tests that headers can be specified when making a request."""
        api_url = f"{BASE}v1/"
        requests_mock.get(f"{BASE}v1/path/to/item", status_code=200)

        api_client = APIClient(api_url)
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "test user agent",
        }
        response = api_client.request(
            "GET",
            "path/to/item",
            headers=headers,
        )
        assert headers.items() <= response.request.headers.items()
