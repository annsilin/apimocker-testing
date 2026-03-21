"""
tests/test_comments.py
"""
import allure
from utils.helpers import NONEXISTENT_ID, get_first_item


@allure.feature("Comments")
class TestCommentsGet:

    @allure.story("Get all comments")
    @allure.title("GET /comments returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_comments_returns_200(self, comments_client):
        assert comments_client.get_comments().status_code == 200

    @allure.story("Get all comments")
    @allure.title("GET /comments?limit=5 returns 200")
    def test_get_comments_with_limit_returns_200(self, comments_client):
        assert comments_client.get_comments(limit=5).status_code == 200

    @allure.story("Get single comment")
    @allure.title("GET /comments/{real_id} returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_comment_by_real_id_returns_200(self, comments_client):
        real_id = get_first_item(comments_client.get_comments()).get("id")
        assert comments_client.get_comment(real_id).status_code == 200

    @allure.story("Get single comment")
    @allure.title("GET /comments/999999 returns 404")
    def test_get_nonexistent_comment_returns_404(self, comments_client):
        resp = comments_client.get_comment(NONEXISTENT_ID)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"


@allure.feature("Comments")
class TestCommentsWrite:
    """
    POST to /comments returns 400 (API validation).
    DELETE returns 204.
    """

    @allure.story("Create comment")
    @allure.title("POST /comments returns 400 (read-only endpoint)")
    def test_post_comment_returns_400(self, comments_client, posts_client):
        post_id = get_first_item(posts_client.get_posts()).get("id")
        resp = comments_client.create_comment(
            {"postId": post_id, "name": "Test", "body": "Test"}
        )
        assert resp.status_code == 400, (
            f"Expected 400 (read-only), got {resp.status_code}"
        )

    @allure.story("Delete comment")
    @allure.title("DELETE /comments/{real_id} returns 200 or 204")
    def test_delete_comment_returns_200_or_204(self, comments_client):
        real_id = get_first_item(comments_client.get_comments()).get("id")
        resp = comments_client.delete_comment(real_id)
        assert resp.status_code in (200, 204), f"Expected 200 or 204, got {resp.status_code}"
