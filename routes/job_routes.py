

from flask import Blueprint, request, jsonify
from models.job import Job
from database import db
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt


job_routes=Blueprint("job_routes",__name__)

@job_routes.route("/api/jobs",methods=["GET"])
@jwt_required(optional=True)
def get_jobs():
    claims = get_jwt()
    role = claims.get("role", "guest") if claims else "guest"
    jobs=Job.query.all()
    results=[job.to_dict(role=role) for job in jobs]
    return jsonify(results),200

@job_routes.route("/api/jobs",methods=["POST"])
@jwt_required()
def post_job():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Access denied"}), 403
    data=request.get_json()
    new_job=Job(
        title=data["title"],
        location=data["location"],
        material_cost=data["material_cost"],
        additional_cost=data["additional_cost"],
        revenue=data["revenue"],
        note=data["note"],
        date=datetime.strptime(data["date"],"%Y-%m-%d").date(),
        is_completed=data.get("is_completed",False)
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({
        "id": new_job.id,
        "title": new_job.title,
        "location": new_job.location,
        "material_cost": new_job.material_cost,
        "additional_cost": new_job.additional_cost,
        "revenue": new_job.revenue,
        "note": new_job.note,
        "date": new_job.date.isoformat(),
        "is_completed": new_job.is_completed
    }), 201

@job_routes.route("/api/jobs/<int:id>",methods=["GET"])
@jwt_required(optional=True)
def get_job(id):
    claims = get_jwt()
    role = claims.get("role", "guest") if claims else "guest"
    job=Job.query.get(id)
    if job:
        return jsonify(job.to_dict(role=role)),200
    else:
        return jsonify({"error":"Job not found."}),404

@job_routes.route("/api/jobs/<int:id>",methods=["PUT"])
@jwt_required()
def put_job(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Access denied"}), 403
    data=request.get_json()
    job=Job.query.get(id)
    if not job:
        return jsonify({"error": "Job not found."}),404
    job.title = data.get("title",job.title)
    job.location = data.get("location",job.location)
    job.material_cost = data.get("material_cost",job.material_cost)
    job.additional_cost = data.get("additional_cost",job.additional_cost)
    job.revenue = data.get("revenue",job.revenue)
    job.note = data.get("note",job.note)
    if "date" in data:
        job.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    job.is_completed = data.get("is_completed",job.is_completed)

    db.session.commit()

    return jsonify(job.to_dict()),200

@job_routes.route("/api/jobs/<int:id>",methods=["DELETE"])
@jwt_required()
def delete_job(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Access denied"}), 403
    job=Job.query.get(id)
    if not job:
        return jsonify({"error": "Job not found."}), 404
    db.session.delete(job)
    db.session.commit()



    return jsonify({"message": "Job deleted successfully"}),200

@job_routes.route("/api/jobs/<int:id>/done",methods=["PATCH"])
@jwt_required()
def patch_job(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Access denied"}), 403
    job=Job.query.get(id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    job.is_completed = True
    db.session.commit()
    return jsonify({"message":"Job marked as completed","job":job.to_dict()}), 200