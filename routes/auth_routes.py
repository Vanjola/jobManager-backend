import os
from dotenv import  load_dotenv

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

load_dotenv()




auth_routes=Blueprint("auth_routes",__name__)

@auth_routes.route("/api/jobs/login",methods=["POST"])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")



    if username!=os.getenv("ADMIN_USERNAME") or password!=os.getenv("ADMIN_PASSWORD"):
        return jsonify({"error":"Invalid credentials"}),401

    access_token=create_access_token(
        identity=username,
        additional_claims={"role":"admin"}
    )

    return jsonify({"access_token": access_token}),200