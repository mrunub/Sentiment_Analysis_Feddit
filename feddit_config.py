"""
Defines URLs and query parameters for interacting with an API.
"""

# Define the URL of the endpoints

SUBFEDDITS_URL = "http://localhost:8080/api/v1/subfeddits"
SUBFEDDIT_URL = "http://localhost:8080/api/v1/subfeddit"
COMMENTS_URL = "http://localhost:8080/api/v1/comments"

# Define query parameters

SUBFEDDITS_PARAMS = {
    "skip": 0,
    "limit": 3
}

SUBFEDDIT_PARAMS = {
    "subfeddit_id": 1
}

COMMENTS_PARAMS = {
    "subfeddit_id": 1,
    "skip": 0,
    "limit": 10
}
