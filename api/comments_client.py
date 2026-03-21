"""
api/comments_client.py
-----------------------
API Layer - client for /comments resource.
"""

import allure
import requests

from api.base_client import BaseClient

RESOURCE = "comments"


class CommentsClient(BaseClient):
    """Client for the /comments endpoint."""

    @allure.step("GET /comments - get all comments")
    def get_comments(self, **params) -> requests.Response:
        return self.get(RESOURCE, params=params)

    @allure.step("GET /comments/{comment_id} - get comment by id")
    def get_comment(self, comment_id: int) -> requests.Response:
        return self.get(f"{RESOURCE}/{comment_id}")

    @allure.step("POST /comments - create comment")
    def create_comment(self, payload: dict) -> requests.Response:
        return self.post(RESOURCE, json=payload)

    @allure.step("PUT /comments/{comment_id} - full update")
    def update_comment(self, comment_id: int, payload: dict) -> requests.Response:
        return self.put(f"{RESOURCE}/{comment_id}", json=payload)

    @allure.step("PATCH /comments/{comment_id} - partial update")
    def patch_comment(self, comment_id: int, payload: dict) -> requests.Response:
        return self.patch(f"{RESOURCE}/{comment_id}", json=payload)

    @allure.step("DELETE /comments/{comment_id} - delete comment")
    def delete_comment(self, comment_id: int) -> requests.Response:
        return self.delete(f"{RESOURCE}/{comment_id}")
