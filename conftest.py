"""
conftest.py
-----------
Test Infrastructure Layer.
"""

import logging
import os

import pytest

from api.users_client import UsersClient
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

@pytest.fixture(scope="session", autouse=True)
def _setup_dirs():
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    logger.info("Output directories ready.")
