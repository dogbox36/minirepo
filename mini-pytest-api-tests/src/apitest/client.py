import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import settings

# Configure logger
logger = logging.getLogger("api_client")
logger.setLevel(logging.INFO)
# Basic handler if not configured elsewhere (pytest usually captures logs)
if not logger.handlers:
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(c_handler)


class ApiClient:
    def __init__(self, base_url: str = settings.base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        # Setup Retries
        retries = Retry(
            total=settings.retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # Auth headers if token is present
        if settings.api_token:
            self.session.headers.update({"Authorization": f"Bearer {settings.api_token}"})

        # Set a custom User-Agent to avoid being blocked
        self.session.headers.update({"User-Agent": "Mini-Pytest-Api-Test/1.0"})

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Quick logging (redact sensitive info in real world)
        logger.info(f"Request: {method} {url}")
        if "json" in kwargs:
            logger.info(f"Payload: {kwargs['json']}")

        try:
            response = self.session.request(method=method, url=url, timeout=settings.timeout, **kwargs)
            # response.raise_for_status()  # Disable automatic raising for tests to assert status codes manually
            # For testing framework, usually we WANT to see 4xx/5xx in tests, so maybe don't raise automatically
            # UNLESS it's a connection error.
            # requests.raise_for_status() raises for 4xx/5xx.
            # In tests we often check `assert response.status_code == 400`.
            # So let's catch raise_for_status, log it, but return response to test?
            # Or just don't raise it.

            logger.info(f"Response: {response.status_code} - {response.elapsed.total_seconds()}s")
            return response

        except requests.RequestException as e:
            logger.error(f"Request Failed: {e}")
            raise

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)
