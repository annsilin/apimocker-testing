"""
tests/test_health.py
---------------------
Verifies the API is reachable and returns 200.
"""

import allure


@allure.feature("Health")
@allure.story("Health check")
class TestHealth:

    @allure.title("GET /health returns 200")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_health_check_returns_200(self, health_client):
        """API must be reachable and respond with 200 OK."""
        response = health_client.get_health()
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )
