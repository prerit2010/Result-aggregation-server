from app import db
import datetime

class UserSystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_dist = db.Column(db.String)
    uname  = db.Column(db.String)
    version = db.Column(db.String)
    system = db.Column(db.String)
    machine = db.Column(db.String)
    system_platform = db.Column(db.String) 
    uname = db.Column(db.String)
    python_version = db.Column(db.String)
    workshop_id = db.Column(db.String)
    email_id = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

class SuccessfulInstalls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    version = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=db.func.now())