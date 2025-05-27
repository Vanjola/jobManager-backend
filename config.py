import os
from dotenv import load_dotenv

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR,'jobmanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")