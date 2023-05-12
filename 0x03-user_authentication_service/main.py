import requests
from requests.exceptions import HTTPError

BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    msg = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401
    print("Login with wrong password failed as expected.")


def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    print("Login successful.")
    return session_id


def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403
    print("Accessing profile without logging in failed as expected.")


def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == EMAIL
    print("Profile accessed successfully.")


def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/logout"
    cookies = {"session_id": session_id}
    response = requests.post(url, cookies=cookies)
    assert response.status_code == 200
    print("Logout successful.")


def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    reset_token = response.json()["reset_token"]
    print("Reset password token received.")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200
    print("Password updated successfully.")


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
