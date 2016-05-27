from flask import Flask, jsonify, make_response
from app import app, db
from flask import request
from models import UserSystemInfo

@app.route('/installation_data/', methods=['POST'])
def installation_data():

    user_system_info = request.json.get('user_system_info', None)

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

    try:
        user_info = UserSystemInfo(system_dist=system_dist, python_version=python_version,\
                                uname=uname, version=version, system=system, \
                                machine=machine, system_platform=system_platform, \
                                workshop_id=workshop_id, email_id=workshop_id)
        db.session.add(user_info)
        db.session.commit()
    except:
        success = False
        summary = "Something bad happened"
    else:
        success = True
        summary = "Successful"
    
    response = {"status" : success, "summary" : summary}
    return make_response(jsonify(response))