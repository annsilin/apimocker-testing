"""
utils/helpers.py
-----------------
Shared test utilities.
"""

import time

# A large integer ID that doesn't exist in the API.
NONEXISTENT_ID = 999999


def extract_id(response) -> str:
    """Extract the resource ID from an API response."""
    body = response.json()
    if isinstance(body, dict):
        obj = body.get("data", body)
        if isinstance(obj, dict):
            val = obj.get("id") or obj.get("_id")
            return str(val) if val is not None else None
    return None


def get_first_item(list_response) -> dict:
    """Extract the first item from a list response."""
    data = list_response.json()
    items = data.get("data", data) if isinstance(data, dict) else data
    assert items, "Empty list returned"
    return items[0]


def unique_email() -> str:
    """Return a unique email address to avoid 409 Conflict."""
    return f"test.{int(time.time() * 1000)}@example.com"


def unique_username() -> str:
    """Return a unique username."""
    return f"user{int(time.time() * 1000)}"
