import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
from db_manager import DbManager
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

SECRET_KEY = "temp-secret-key"

# '''
# Users Schema:
# user_id: String, Required, Unique
# email: String, Required, Unique
# username: String, Required, Unique
# password: String, Required
# created_at: Date, Required

# Plans Schema:
# plan_id: String, Required, Unique
# user_id: String, Required
# title: String, Required
# days: Int, Required
# created_at: Date, Required

# Tasks Schema:
# task_id: String, Required, Unique
# plan_id: String, Required
# day: Int, Required
# description: String, Required
# completed: Boolean, Required
# '''

@app.route("/users/register", methods=["POST"])
def register():
    try:
        current_time = datetime.now(timezone.utc)
        data = request.get_json()
        if not data or "email" not in data or "username" not in data or "password" not in data:
            jsonify(message="Missing user info", error="Bad request"), 400
        user = db_manager().create_user(data["email"], data["username"], data["password"], current_time)
        token = jwt.encode(
            {
                "user_id": user["user_id"],
                "email": user["email"],
                "username": user["username"],
                "created_at": user["created_at"]
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        return jsonify(token=token), 200
    except Exception as e:
        return jsonify(message="Something went wrong", error=str(e)), 500

@app.route("/users/login", methods=["POST"])
def login():
    try:
        
    except Exception as e:


if __name__ == "__main__":
    app.run(port=5000, debug=False)