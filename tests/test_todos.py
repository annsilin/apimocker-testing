"""
tests/test_todos.py
"""
import allure
from utils.helpers import NONEXISTENT_ID, extract_id, get_first_item

def _get_user_id(users_client):
    return get_first_item(users_client.get_users()).get("id")


@allure.feature("Todos")
class TestTodosGet:

    @allure.story("Get all todos")
    @allure.title("GET /todos returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_todos_returns_200(self, todos_client):
        assert todos_client.get_todos().status_code == 200

    @allure.story("Get all todos")
    @allure.title("GET /todos?limit=5 returns 200")
    def test_get_todos_with_limit_returns_200(self, todos_client):
        assert todos_client.get_todos(limit=5).status_code == 200

    @allure.story("Get single todo")
    @allure.title("GET /todos/{real_id} returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_todo_by_real_id_returns_200(self, todos_client):
        real_id = get_first_item(todos_client.get_todos()).get("id")
        assert todos_client.get_todo(real_id).status_code == 200

    @allure.story("Get single todo")
    @allure.title("GET /todos/999999 returns 404")
    def test_get_nonexistent_todo_returns_404(self, todos_client):
        resp = todos_client.get_todo(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"


@allure.feature("Todos")
class TestTodosPost:

    @allure.story("Create todo")
    @allure.title("POST /todos returns 201")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_todo_returns_201(self, todos_client, users_client):
        user_id = _get_user_id(users_client)
        resp = todos_client.create_todo({"title": "Buy groceries", "completed": False, "userId": user_id})
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"


@allure.feature("Todos")
class TestTodosPut:

    @allure.story("Update todo")
    @allure.title("PUT /todos/{real_id} returns 200")
    def test_update_todo_returns_200(self, todos_client, users_client):
        user_id = _get_user_id(users_client)
        real_id = get_first_item(todos_client.get_todos()).get("id")
        resp = todos_client.update_todo(real_id, {"title": "Updated", "completed": True, "userId": user_id})
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    @allure.story("Update todo")
    @allure.title("PUT /todos/999999 returns 404")
    def test_update_nonexistent_todo_returns_404(self, todos_client):
        resp = todos_client.update_todo(NONEXISTENT_ID, {"title": "Ghost"})
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"


@allure.feature("Todos")
class TestTodosPatch:

    @allure.story("Partial update todo")
    @allure.title("PATCH /todos/{real_id} returns 400 (not supported)")
    def test_patch_todo_returns_400(self, todos_client):
        """PATCH is not supported for /todos."""
        real_id = get_first_item(todos_client.get_todos()).get("id")
        resp = todos_client.patch_todo(real_id, {"completed": True})
        assert resp.status_code == 400, f"Expected 400 (not supported), got {resp.status_code}"


@allure.feature("Todos")
class TestTodosDelete:

    @allure.story("Delete todo")
    @allure.title("DELETE /todos/{created_id} returns 200 or 204")
    def test_delete_todo_returns_200_or_204(self, todos_client, users_client):
        user_id = _get_user_id(users_client)
        created = todos_client.create_todo({"title": "Del", "completed": False, "userId": user_id})
        assert created.status_code == 201
        todo_id = extract_id(created)
        resp = todos_client.delete_todo(todo_id)
        assert resp.status_code in (200, 204), f"Expected 200/204, got {resp.status_code}"

    @allure.story("Delete todo")
    @allure.title("DELETE /todos/999999 returns 404")
    def test_delete_nonexistent_todo_returns_404(self, todos_client):
        resp = todos_client.delete_todo(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
