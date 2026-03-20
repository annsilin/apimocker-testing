"""
api/users_client.py
--------------------
API Layer - client for /users resource.
"""

import allure
import requests

from api.base_client import BaseClient

RESOURCE = "users"


class UsersClient(BaseClient):
    """Client for the /users endpoint."""

    @allure.step("GET /users - get all users")
    def get_users(self, **params) -> requests.Response:
        """GET /users - returns a list of users."""
        return self.get(RESOURCE, params=params)

    @allure.step("GET /users/{user_id} - get user by id")
    def get_user(self, user_id) -> requests.Response:
        """GET /users/{id} - returns a single user."""
        return self.get(f"{RESOURCE}/{user_id}")

    @allure.step("POST /users - create user")
    def create_user(self, payload: dict) -> requests.Response:
        """POST /users - creates a new user."""
        return self.post(RESOURCE, json=payload)

    @allure.step("PUT /users/{user_id} - full update")
    def update_user(self, user_id, payload: dict) -> requests.Response:
        """PUT /users/{id} - replaces the user object."""
        return self.put(f"{RESOURCE}/{user_id}", json=payload)

    @allure.step("PATCH /users/{user_id} - partial update")
    def patch_user(self, user_id, payload: dict) -> requests.Response:
        """PATCH /users/{id} - partially updates the user."""
        return self.patch(f"{RESOURCE}/{user_id}", json=payload)

    @allure.step("DELETE /users/{user_id} - delete user")
    def delete_user(self, user_id) -> requests.Response:
        """DELETE /users/{id} - removes the user."""
        return self.delete(f"{RESOURCE}/{user_id}")
