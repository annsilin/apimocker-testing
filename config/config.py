"""
config/config.py
----------------
Config Layer.
"""

import os

# Target API
BASE_URL: str = os.getenv("BASE_URL", "https://apimocker.com")

# Timeouts (seconds)
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "15"))

# Default headers
DEFAULT_HEADERS: dict = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Output paths
ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
