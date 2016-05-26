from flask import Flask, jsonify, make_response
from app import app, db
from flask import request
from models import UserSystemInfo

@app.route('/installation_data/', methods=['POST'])
def installation_data():

    system_dist = request.json.get('system_dist', None)
    uname  = request.json.get('uname', None)
    version = request.json.get('version', None)
    system = request.json.get('system', None)
    machine = request.json.get('machine', None)
    system_platform = request.json.get('system_platform', None)
    uname = request.json.get('uname', None)
    python_version = request.json.get('python_version', None)
    workshop_id = request.json.get('workshop_id', None)
    email_id = request.json.get('email_id', None)
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