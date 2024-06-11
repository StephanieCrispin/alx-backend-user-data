from flask import Flask, jsonify, request, redirect
from flask import abort, url_for
from flask_cors import (CORS)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route("/", methods=["GET"], strict_slashes=False)
def get_basic():
    """Gets root route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def user():
    """A Funky documentation"""
    email = request.form.email
    password = request.form.password
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except Exception:
        pass

    return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Login user documentation"""
    email = request.form.email
    password = request.form.password

    if AUTH.valid_login(email, password) is False:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Deletes a user session and logs out"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_session()
        return redirect(url_for(get_basic))
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Use session cookie to get user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)
    return jsonify({"email": user["email"]})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Gets a token for reset password"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    email = request.form.email
    password = request.form.new_password
    reset_token = request.form.reset_token
    try:
        AUTH.update_password(reset_token=reset_token, password=password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
