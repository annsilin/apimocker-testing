"""
api/todos_client.py
--------------------
API Layer - client for /todos resource.
"""

import allure
import requests

from api.base_client import BaseClient

RESOURCE = "todos"


class TodosClient(BaseClient):
    """Client for the /todos endpoint."""

    @allure.step("GET /todos - get all todos")
    def get_todos(self, **params) -> requests.Response:
        return self.get(RESOURCE, params=params)

    @allure.step("GET /todos/{todo_id} - get todo by id")
    def get_todo(self, todo_id) -> requests.Response:
        return self.get(f"{RESOURCE}/{todo_id}")

    @allure.step("POST /todos - create todo")
    def create_todo(self, payload: dict) -> requests.Response:
        return self.post(RESOURCE, json=payload)

    @allure.step("PUT /todos/{todo_id} - full update")
    def update_todo(self, todo_id, payload: dict) -> requests.Response:
        return self.put(f"{RESOURCE}/{todo_id}", json=payload)

    @allure.step("PATCH /todos/{todo_id} - partial update")
    def patch_todo(self, todo_id, payload: dict) -> requests.Response:
        return self.patch(f"{RESOURCE}/{todo_id}", json=payload)

    @allure.step("DELETE /todos/{todo_id} - delete todo")
    def delete_todo(self, todo_id) -> requests.Response:
        return self.delete(f"{RESOURCE}/{todo_id}")
