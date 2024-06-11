#!/usr/bin/env python3
"""Integration tests in python with requests module"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

email = "bob@bob.com"
password = "MyPwdOfBob"
base_url = "http://127.0.0.1:5000/"


def register_user(email: str, password: str) -> None:
    """tests /users endpoint"""
    data = {"email": email, "password": password}
    url = base_url + "users"
    r = requests.post(url, data=data)
    assert 200 == r.status_code
    assert {"email": email, "message": "user created"} == r.json()


def log_in_wrong_password(email: str, password: str) -> None:
    """logs in with wrong password"""
    data = {"email": email, "password": "wrong password"}
    url = base_url + "sessions"
    r = requests.post(url, data=data)
    assert 401 == r.status_code


def log_in(email: str, password: str) -> str:
    """logs in properly"""
    data = {"email": email, "password": password}
    url = base_url + "sessions"
    r = requests.post(url, data=data)
    cookie = r.cookies["session_id"]
    assert 200 == r.status_code
    assert isinstance(cookie, str)
    return cookie


def profile_unlogged() -> None:
    """unlogs profile"""

    url = base_url + "profile"
    cookie = {"session_id": "wrong cookie"}
    r = requests.get(url, cookies=cookie)
    assert 403 == r.status_code


def profile_logged(session_id: str) -> None:
    """logs in profile"""
    url = base_url + "profile"
    cookie = {"session_id": session_id}
    r = requests.get(url, cookies=cookie)
    assert 200 == r.status_code
    assert {"email": EMAIL} == r.json()


def log_out(session_id: str) -> None:
    """logs out profile"""
    url = base_url + "sessions"
    cookie = {"session_id": session_id}
    r = requests.delete(url, cookie=cookie)
    assert 200 == r.status_code


def reset_password_token(email: str) -> str:
    """generates reset password token"""
    url = base_url + "reset_password"
    data = {
        "email": email,
    }
    r = requests.post(url, data=data)
    assert 200 == r.status_code
    token = r.json()["reset_token"]
    assert len(token) == 36
    return token


def update_password(email: str, reset_token: str):
    """updates new password"""
    url = base_url + "reset_password"
    data = {
        "email": email,
        "reset_token": reset_token
    }
    r = requests.put(url, data=data)
    assert 200 == r.status_code
    assert {"email": email, "message": "Password updated"} == r.json()


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
