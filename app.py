from flask import Flask
from config import Config
from database import db
from routes.job_routes import job_routes



app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(job_routes)

@app.route("/",methods=["GET"])
def home():
    return "JobManager API is running!"










if __name__=="__main__":
    app.run(debug=True)