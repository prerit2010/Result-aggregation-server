from flask import Flask, jsonify, make_response
from app import application, db
from flask import request
from models import UserSystemInfo, SuccessfulInstalls, FailedInstalls, Attempts
import uuid

@application.errorhandler(500)
def internal_error(error):
    db.session.rollback()

@application.route('/installation_data/', methods=['POST'])
def installation_data():
    user_system_info = request.json.get('user_system_info')
    successful_installs = request.json.get('successful_installs')
    failed_installs = request.json.get('failed_installs')
    unique_user_id = request.json.get('unique_user_id')
    if unique_user_id is None:
        unique_user_id = str(uuid.uuid4())
        message = "new id generated"
        user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
        while(user_info): # Resolving Collision
            unique_user_id = str(uuid.uuid4())
            user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
    else:
        message = "pushed data with same id"
        """ Check whether the received unique id has already an associated record 
            in the database, or is it accidently changed by the user.
        """
        user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
        if user_info is None:
            unique_user_id = str(uuid.uuid4())
            message = "new id generated"

    distribution_name = user_system_info.get('distribution_name')
    distribution_version = user_system_info.get('distribution_version')
    system_version = user_system_info.get('system_version')
    system = user_system_info.get('system')
    machine = user_system_info.get('machine')
    system_platform = user_system_info.get('system_platform')
    python_version = user_system_info.get('python_version')
    workshop_id = user_system_info.get('workshop_id')
    email_id = user_system_info.get('email_id')
    # uname  = user_system_info.get('uname')

    attempt = Attempts(unique_user_id=unique_user_id)
   
    success_objects_list = [
        SuccessfulInstalls(name=succ_install.get('name'),version=succ_install.get('version')) 
            for succ_install in successful_installs 
    ]

    failed_objects_list = [
        FailedInstalls(name=fail_install.get('name'), version=fail_install.get('version'),
             error_description=fail_install.get('error_description')) 
            for fail_install in failed_installs
    ]
    
    user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
    if user_info is None:
        user_info = UserSystemInfo(distribution_name=distribution_name, 
                    distribution_version=distribution_version, system_version=system_version,
                    system=system, machine=machine, system_platform=system_platform,
                    workshop_id=workshop_id, email_id=email_id,
                    python_version=python_version, unique_user_id=unique_user_id)
    
    user_info.successful_installs.extend(success_objects_list)
    user_info.failed_installs.extend(failed_objects_list)
    attempt.successful_installs.extend(success_objects_list)
    attempt.failed_installs.extend(failed_objects_list)
    db.session.add(attempt)
    db.session.add(user_info)
    db.session.add_all(success_objects_list)
    db.session.add_all(failed_objects_list)
    
    try:
        db.session.commit()
    except:
        summary = {"status": "Something bad happened"}
    else:
        summary = {"status": "Successful"}
    summary['message'] = message
    response = {'key': unique_user_id, 'summary' : summary}
    return make_response(jsonify(response))

@application.route('/')
def default():
    return "<h1 style='color:blue'>Hello There!</h1>"