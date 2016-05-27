from flask import Flask, jsonify, make_response
from app import app, db
from flask import request
from models import UserSystemInfo, SuccessfulInstalls, FailedInstalls

@app.route('/installation_data/', methods=['POST'])
def installation_data():

    user_system_info = request.json.get('user_system_info', None)
    successful_installs = request.json.get('successful_installs', None)
    failed_installs = request.json.get('failed_installs', None)

    system_dist = user_system_info.get('system_dist', None)
    uname  = user_system_info.get('uname', None)
    version = user_system_info.get('version', None)
    system = user_system_info.get('system', None)
    machine = user_system_info.get('machine', None)
    system_platform = user_system_info.get('system_platform', None)
    uname = user_system_info.get('uname', None)
    python_version = user_system_info.get('python_version', None)
    workshop_id = user_system_info.get('workshop_id', None)
    email_id = user_system_info.get('email_id', None)

    success_objects_list = []
    for succ_install in successful_installs:
        obj = SuccessfulInstalls(name=succ_install.get('name', None), \
                version=succ_install.get('version', None))
        success_objects_list.append(obj)

    failed_objects_list = []
    for fail_install in failed_installs:
        obj = FailedInstalls(name=fail_install.get('name', None),\
                version=fail_install.get('version', None), \
                error_description=fail_install.get('error_description', None), \
                error_cause=fail_install.get('error_cause', None))
        failed_objects_list.append(obj)

    user_info = UserSystemInfo(system_dist=system_dist, python_version=python_version,\
                            uname=uname, version=version, system=system, \
                            machine=machine, system_platform=system_platform, \
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