"""
tests/test_posts.py
"""
import allure
from utils.helpers import NONEXISTENT_ID, extract_id, get_first_item


def _get_user_id(users_client):
    return get_first_item(users_client.get_users()).get("id")


@allure.feature("Posts")
class TestPostsGet:

    @allure.story("Get all posts")
    @allure.title("GET /posts returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_posts_returns_200(self, posts_client):
        assert posts_client.get_posts().status_code == 200

    @allure.story("Get all posts")
    @allure.title("GET /posts?limit=3 returns 200")
    def test_get_posts_with_limit_returns_200(self, posts_client):
        assert posts_client.get_posts(limit=3).status_code == 200

    @allure.story("Get single post")
    @allure.title("GET /posts/{real_id} returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_post_by_real_id_returns_200(self, posts_client):
        real_id = get_first_item(posts_client.get_posts()).get("id")
        assert posts_client.get_post(real_id).status_code == 200

    @allure.story("Get single post")
    @allure.title("GET /posts/999999 returns 404")
    def test_get_nonexistent_post_returns_404(self, posts_client):
        resp = posts_client.get_post(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"

    @allure.story("Search posts")
    @allure.title("GET /posts/search?q=development returns 200")
    def test_search_posts_returns_200(self, posts_client):
        assert posts_client.search_posts("development").status_code == 200


@allure.feature("Posts")
class TestPostsPost:

    @allure.story("Create post")
    @allure.title("POST /posts returns 201")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_post_returns_201(self, posts_client, users_client):
        user_id = _get_user_id(users_client)
        resp = posts_client.create_post({"title": "Test Post", "body": "Body", "userId": user_id})
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"


@allure.feature("Posts")
class TestPostsPut:

    @allure.story("Update post")
    @allure.title("PUT /posts/{real_id} returns 200")
    def test_update_post_returns_200(self, posts_client, users_client):
        user_id = _get_user_id(users_client)
        real_id = get_first_item(posts_client.get_posts()).get("id")
        resp = posts_client.update_post(real_id, {"title": "Updated", "body": "Updated", "userId": user_id})
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    @allure.story("Update post")
    @allure.title("PUT /posts/999999 returns 400 or 404")
    def test_update_nonexistent_post_returns_error(self, posts_client):
        """API returns 400 for PUT on nonexistent resource (missing required fields)."""
        resp = posts_client.update_post(NONEXISTENT_ID, {"title": "Ghost"})
        assert resp.status_code in (400, 404), f"Expected 400 or 404, got {resp.status_code}"


@allure.feature("Posts")
class TestPostsPatch:

    @allure.story("Partial update post")
    @allure.title("PATCH /posts/{real_id} returns 400 (not supported)")
    def test_patch_post_returns_400(self, posts_client):
        """PATCH is not supported for /posts on apimocker.com."""
        real_id = get_first_item(posts_client.get_posts()).get("id")
        resp = posts_client.patch_post(real_id, {"title": "Patched"})
        assert resp.status_code == 400, f"Expected 400 (not supported), got {resp.status_code}"


@allure.feature("Posts")
class TestPostsDelete:

    @allure.story("Delete post")
    @allure.title("DELETE /posts/{created_id} returns 200 or 204")
    def test_delete_post_returns_200_or_204(self, posts_client, users_client):
        user_id = _get_user_id(users_client)
        created = posts_client.create_post({"title": "Del", "body": "Body", "userId": user_id})
        assert created.status_code == 201
        post_id = extract_id(created)
        resp = posts_client.delete_post(post_id)
        assert resp.status_code in (200, 204), f"Expected 200/204, got {resp.status_code}"

    @allure.story("Delete post")
    @allure.title("DELETE /posts/999999 returns 404")
    def test_delete_nonexistent_post_returns_404(self, posts_client):
        resp = posts_client.delete_post(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
