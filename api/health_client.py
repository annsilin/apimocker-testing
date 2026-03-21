"""
api/health_client.py
---------------------
API Layer - client for /health endpoint.
"""

import allure
import requests

from api.base_client import BaseClient


class HealthClient(BaseClient):
    """Client for the /health endpoint."""

    @allure.step("GET /health - health check")
    def get_health(self) -> requests.Response:
        """GET /health - returns API health status."""
        return self.get("health")
