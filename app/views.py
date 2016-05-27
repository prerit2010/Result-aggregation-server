from flask import Flask, jsonify, make_response
from app import app, db
from flask import request
from models import UserSystemInfo, SuccessfulInstalls, FailedInstalls

@app.route('/installation_data/', methods=['POST'])
def installation_data():

    user_system_info = request.json.get('user_system_info')
    successful_installs = request.json.get('successful_installs')
    failed_installs = request.json.get('failed_installs')

    system_dist = user_system_info.get('system_dist')
    uname  = user_system_info.get('uname')
    version = user_system_info.get('version')
    system = user_system_info.get('system')
    machine = user_system_info.get('machine')
    system_platform = user_system_info.get('system_platform')
    uname = user_system_info.get('uname')
    python_version = user_system_info.get('python_version')
    workshop_id = user_system_info.get('workshop_id')
    email_id = user_system_info.get('email_id')

    success_objects_list = [
        SuccessfulInstalls(name=succ_install.get('name'),
            version=succ_install.get('version')) 
            for succ_install in successful_installs 
    ]

    failed_objects_list = [
        FailedInstalls(name=fail_install.get('name'), version=fail_install.get('version'),
            error_description=fail_install.get('error_description'),
            error_cause=fail_install.get('error_cause')) 
            for fail_install in failed_installs 
    ]

    user_info = UserSystemInfo(system_dist=system_dist, python_version=python_version,
                    uname=uname, version=version, system=system,
                    machine=machine, system_platform=system_platform,
                    workshop_id=workshop_id, email_id=workshop_id)
    
    user_info.successful_installs.extend(success_objects_list)
    user_info.failed_installs.extend(failed_objects_list)
    db.session.add(user_info)
    db.session.add_all(success_objects_list)
    db.session.add_all(failed_objects_list)
    
    try:
        db.session.commit()
    except:
        success = False
        summary = "Something bad happened"
    else:
        success = True
        summary = "Successful"
    
    response = {"status" : success, "summary" : summary}
    return make_response(jsonify(response))