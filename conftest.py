"""
conftest.py
-----------
Test Infrastructure Layer.
"""

import logging
import os

import pytest

from api.users_client import UsersClient
from api.comments_client import CommentsClient
from api.health_client import HealthClient
from api.posts_client import PostsClient
from api.todos_client import TodosClient
from config.config import ALLURE_RESULTS_DIR, BASE_URL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("conftest")


@pytest.fixture(scope="session")
def users_client() -> UsersClient:
    return UsersClient(BASE_URL)

@pytest.fixture(scope="session")
def posts_client() -> PostsClient:
    return PostsClient(BASE_URL)

@pytest.fixture(scope="session")
def todos_client() -> TodosClient:
    return TodosClient(BASE_URL)

@pytest.fixture(scope="session")
def comments_client() -> CommentsClient:
    return CommentsClient(BASE_URL)

@pytest.fixture(scope="session")
def health_client() -> HealthClient:
    return HealthClient(BASE_URL)

@pytest.fixture(scope="session", autouse=True)
def _setup_dirs():
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    logger.info("Output directories ready.")
