"""
api/base_client.py
------------------
Infrastructure Layer - base HTTP client.
"""

import logging

import allure
import requests

from config.config import DEFAULT_HEADERS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BaseClient:
    """Base HTTP client."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    # Private helpers
    def _url(self, path: str) -> str:
        """Build full URL from base_url + path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        logger.info("→ %s %s  params=%s  body=%s",
                    method.upper(), url,
                    kwargs.get("params"), kwargs.get("json"))

    def _log_response(self, response: requests.Response) -> None:
        logger.info("← %s %s  [%d]  %.0fms",
                    response.request.method,
                    response.url,
                    response.status_code,
                    response.elapsed.total_seconds() * 1000)
        logger.debug("   body: %s", response.text[:500])

    def _attach_to_allure(self, response: requests.Response) -> None:
        """Attach request/response details to the current Allure step."""
        allure.attach(
            f"URL:    {response.url}\n"
            f"Method: {response.request.method}\n"
            f"Status: {response.status_code}\n"
            f"Time:   {response.elapsed.total_seconds() * 1000:.0f} ms\n"
            f"Body:   {response.text[:1000]}",
            name="HTTP Response",
            attachment_type=allure.attachment_type.TEXT,
        )

    def _send(self, method: str, path: str, **kwargs) -> requests.Response:
        """Send HTTP request, log it, attach to Allure, return response."""
        url = self._url(path)
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        self._log_request(method, url, **kwargs)
        response = self.session.request(method, url, **kwargs)
        self._log_response(response)
        self._attach_to_allure(response)
        return response

    # Public HTTP methods

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._send("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._send("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._send("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._send("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._send("DELETE", path, **kwargs)
