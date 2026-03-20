"""
tests/test_users.py
"""
import allure
from utils.helpers import NONEXISTENT_ID, extract_id, get_first_item, unique_email, unique_username


@allure.feature("Users")
class TestUsersGet:

    @allure.story("Get all users")
    @allure.title("GET /users returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_users_returns_200(self, users_client):
        assert users_client.get_users().status_code == 200

    @allure.story("Get all users")
    @allure.title("GET /users?limit=5 returns 200")
    def test_get_users_with_limit_returns_200(self, users_client):
        assert users_client.get_users(limit=5).status_code == 200

    @allure.story("Get single user")
    @allure.title("GET /users/{real_id} returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_real_id_returns_200(self, users_client):
        real_id = get_first_item(users_client.get_users()).get("id")
        assert users_client.get_user(real_id).status_code == 200

    @allure.story("Get single user")
    @allure.title("GET /users/999999 returns 404")
    def test_get_nonexistent_user_returns_404(self, users_client):
        resp = users_client.get_user(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"


@allure.feature("Users")
class TestUsersPost:

    @allure.story("Create user")
    @allure.title("POST /users returns 201")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_returns_201(self, users_client):
        resp = users_client.create_user(
            {"name": "Ann Silin", "email": unique_email(), "username": unique_username()}
        )
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"


@allure.feature("Users")
class TestUsersPut:

    @allure.story("Update user")
    @allure.title("PUT /users/{real_id} returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_returns_200(self, users_client):
        # Use existing user from GET list - PUT works on seed data
        real_id = get_first_item(users_client.get_users()).get("id")
        resp = users_client.update_user(real_id, {
            "name": "Updated", "email": unique_email(), "username": unique_username(),
        })
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    @allure.story("Update user")
    @allure.title("PUT /users/999999 returns 404")
    def test_update_nonexistent_user_returns_404(self, users_client):
        resp = users_client.update_user(NONEXISTENT_ID, {
            "name": "Ghost", "email": unique_email(), "username": unique_username(),
        })
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"


@allure.feature("Users")
class TestUsersPatch:

    @allure.story("Partial update user")
    @allure.title("PATCH /users/{real_id} returns 404 or 400 (not supported)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_user_not_supported(self, users_client):
        """PATCH is not supported for /users on apimocker.com."""
        real_id = get_first_item(users_client.get_users()).get("id")
        resp = users_client.patch_user(real_id, {"name": "Patched"})
        assert resp.status_code in (400, 404), f"Expected 400 or 404, got {resp.status_code}"


@allure.feature("Users")
class TestUsersDelete:

    @allure.story("Delete user")
    @allure.title("DELETE /users/{created_id} returns 200 or 204")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_returns_200_or_204(self, users_client):
        created = users_client.create_user(
            {"name": "Del", "email": unique_email(), "username": unique_username()}
        )
        assert created.status_code == 201
        user_id = extract_id(created)
        resp = users_client.delete_user(user_id)
        assert resp.status_code in (200, 204), f"Expected 200/204, got {resp.status_code}"

    @allure.story("Delete user")
    @allure.title("DELETE /users/999999 returns 404")
    def test_delete_nonexistent_user_returns_404(self, users_client):
        resp = users_client.delete_user(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
