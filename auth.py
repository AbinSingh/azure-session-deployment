VALID_USERS = {
    "alice": "password123",
    "bob": "password123"
}


def authenticate(username: str, password: str) -> bool:
    """
    Validate username and password.
    """

    if username not in VALID_USERS:
        return False

    return VALID_USERS[username] == password