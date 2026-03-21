"""
api/posts_client.py
--------------------
API Layer - client for /posts resource.
"""

import allure
import requests

from api.base_client import BaseClient

RESOURCE = "posts"


class PostsClient(BaseClient):
    """Client for the /posts endpoint."""

    @allure.step("GET /posts - get all posts")
    def get_posts(self, **params) -> requests.Response:
        return self.get(RESOURCE, params=params)

    @allure.step("GET /posts/{post_id} - get post by id")
    def get_post(self, post_id) -> requests.Response:
        return self.get(f"{RESOURCE}/{post_id}")

    @allure.step("POST /posts - create post")
    def create_post(self, payload: dict) -> requests.Response:
        return self.post(RESOURCE, json=payload)

    @allure.step("PUT /posts/{post_id} - full update")
    def update_post(self, post_id, payload: dict) -> requests.Response:
        return self.put(f"{RESOURCE}/{post_id}", json=payload)

    @allure.step("PATCH /posts/{post_id} - partial update")
    def patch_post(self, post_id, payload: dict) -> requests.Response:
        return self.patch(f"{RESOURCE}/{post_id}", json=payload)

    @allure.step("DELETE /posts/{post_id} - delete post")
    def delete_post(self, post_id) -> requests.Response:
        return self.delete(f"{RESOURCE}/{post_id}")

    @allure.step("GET /posts/search?q={query} - search posts")
    def search_posts(self, query: str) -> requests.Response:
        """GET /posts/search?q=... - search by title and content."""
        return self.get(f"{RESOURCE}/search", params={"q": query})

    @allure.step("GET /posts/{post_id}/likes - get post likes")
    def get_post_likes(self, post_id) -> requests.Response:
        return self.get(f"{RESOURCE}/{post_id}/likes")

    @allure.step("POST /posts/{post_id}/likes - add like")
    def like_post(self, post_id, payload: dict = None) -> requests.Response:
        return self.post(f"{RESOURCE}/{post_id}/likes", json=payload or {})
