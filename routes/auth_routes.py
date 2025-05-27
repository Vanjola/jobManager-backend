from venv import create

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token



users = {
    "tata": {
        "password": "1234",
        "role": "admin"
    },
    "gost": {
        "password": "1234",
        "role": "guest"
    }
}


auth_routes=Blueprint("auth_routes",__name__)

@auth_routes.route("/api/jobs/login",methods=["POST"])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")

    user=users.get(username)

    if not user or user["password"]!=password:
        return jsonify({"error":"Invalid credentials"}),401

    access_token=create_access_token(
        identity=username,
        additional_claims={"role":user["role"]}
    )

    return jsonify({"access_token": access_token}),200