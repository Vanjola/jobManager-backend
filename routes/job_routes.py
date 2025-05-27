

from flask import Blueprint, request, jsonify
from models.job import Job
from database import db
from datetime import datetime

job_routes=Blueprint("job_routes",__name__)

@job_routes.route("/api/jobs",methods=["GET"])
def get_jobs():
    jobs=Job.query.all()
    results=[job.to_dict() for job in jobs]
    return jsonify(results)

@job_routes.route("/api/jobs",methods=["POST"])
def post_job():
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
def get_job(id):
    return f"Hello from get id: {id}"

@job_routes.route("/api/jobs/<int:id>",methods=["PUT"])
def put_job(id):
    return f"Hello from put id:{id}"

@job_routes.route("/api/jobs/<int:id>",methods=["DELETE"])
def delete_job(id):
    return f"Hello from delete id:{id}"

@job_routes.route("/api/jobs/<int:id>/done",methods=["PATCH"])
def patch_job(id):
    return f"Hello from patch id:{id}"