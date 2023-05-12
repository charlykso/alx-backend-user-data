#!/usr/bin/env python3
"""app file"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from typing import Tuple, Union


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """the home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> Tuple[str, int]:
    """register user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email=email, password=password)
        response_msg = {
            'email': user.email,
            'message': 'user created'
        }
        return jsonify(response_msg), 200
    except ValueError:
        response_msg = {"message": "email already registered"}
        return jsonify(response_msg), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """implements login"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Union[abort, redirect]:
    """logout user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """user profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> Union[str, abort]:
    """get reset password token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email=str(email))
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token=str(reset_token),
                             password=str(new_password))
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
