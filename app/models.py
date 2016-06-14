from app import db
import datetime

class UserSystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_user_id = db.Column(db.String, unique=True)
    distribution_name = db.Column(db.String)
    distribution_version = db.Column(db.String)
    # uname  = db.Column(db.String)
    system_version = db.Column(db.String)
    system = db.Column(db.String)
    machine = db.Column(db.String)
    system_platform = db.Column(db.String) 
    python_version = db.Column(db.String)
    workshop_id = db.Column(db.String)
    email_id = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    successful_installs = db.relationship('SuccessfulInstalls', backref='user',
                                        cascade="all,delete", lazy='dynamic')
    failed_installs = db.relationship('FailedInstalls', backref='user', 
                                        cascade="all,delete",lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.email_id

class SuccessfulInstalls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    version = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user_system_info.id'))
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Package %r>' % self.name

class FailedInstalls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    version = db.Column(db.String)
    error_description = db.Column(db.String)
    # error_cause = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user_system_info.id'))
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Package %r>' % self.name

class Attempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_user_id = db.Column(db.String)
    successful_installs = db.relationship('SuccessfulInstalls', backref='attempt',
                                            cascade="all,delete", lazy='dynamic')
    failed_installs = db.relationship('FailedInstalls', backref='attempt',
                                        cascade="all,delete", lazy='dynamic')

    def __repr__(self):
        return '<Attempt: {0}, UUID: {1}>'.format(self.id, self.unique_user_id)