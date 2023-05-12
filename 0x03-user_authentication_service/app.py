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


@app.route('/session', methods=['DELETE'], strict_slashes=False)
def logout() -> Union[abort, redirect]:
    """logout user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')  


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
