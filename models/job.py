from database import db


class Job(db.Model):
    __tablename__="jobs"

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(150), nullable=False)
    material_cost=db.Column(db.Float,nullable=False)
    additional_cost = db.Column(db.Float, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    note=db.Column(db.Text)
    date=db.Column(db.Date,nullable=False)
    is_completed=db.Column(db.Boolean,default=False)

    def to_dict(self,role="guest"):
        base = {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "date": self.date.isoformat(),
            "is_completed": self.is_completed,
            "note": self.note
        }

        if role == "admin":
            base.update({
                "material_cost": self.material_cost,
                "additional_cost": self.additional_cost,
                "revenue": self.revenue

            })

        return base