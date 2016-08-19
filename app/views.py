from flask import jsonify, make_response
from app import application, db
from flask import request, render_template, redirect, url_for
from .models import UserSystemInfo, SuccessfulInstalls, FailedInstalls, Attempts
from .limiter import *
from collections import Counter
import uuid
import datetime
import operator
import json


@application.errorhandler(500)
def internal_error(error):
    db.session.rollback()


@application.route('/installation_data/', methods=['POST'])
@ratelimit(limit=500, per=60 * 60)
def installation_data():
    """
    This endpoint accepts the data from installation test scripts and stores it on the database.
    """

    user_system_info = request.json.get('user_system_info')
    successful_installs = request.json.get('successful_installs')
    failed_installs = request.json.get('failed_installs')
    unique_user_id = request.json.get('unique_user_id')

    # Check whether the unique_user_id is received in the request or not.
    # If not, generate a new id.
    if unique_user_id is None:
        unique_user_id = str(uuid.uuid4())
        message = "new id generated"
        user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
        while(user_info):  # Resolving Collision
            unique_user_id = str(uuid.uuid4())
            user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
    else:
        message = "pushed data with same id"

        # Check whether the received unique id has already an associated record
        # in the database, or is it accidently changed by the user.
        user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
        if user_info is None:
            unique_user_id = str(uuid.uuid4())
            message = "new id generated"

    # Get the system information from 'user_system_info', a dictionary received in the request.
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
    workshop_id_default = "No workshop name provided"

    # Everytime an attempt is made, be it from a new user, or from the same user,
    # log the attempt with the user's unique_user_id
    attempt = Attempts(unique_user_id=unique_user_id)

    # Create lists of objects for failed and succesfully installed packages, so that they can be added
    # using the user_id as foreign key.
    success_objects_list = [
        SuccessfulInstalls(name=succ_install.get('name'), version=succ_install.get('version').replace('\n', ''))
        for succ_install in successful_installs
    ]

    failed_objects_list = [
        FailedInstalls(name=fail_install.get('name'), version=fail_install.get('version').replace('\n', ''),
                       error_description=fail_install.get('error_description'))
        for fail_install in failed_installs
    ]

    # Check whether their already exists a record with this unique_user_id.
    # If yes, update the information, else, create a new record.
    user_info = UserSystemInfo.query.filter_by(unique_user_id=unique_user_id).first()
    if user_info is None:
        if workshop_id is None:
            workshop_id = workshop_id_default
        user_info = UserSystemInfo(distribution_name=distribution_name,
                                   distribution_version=distribution_version, system_version=system_version,
                                   system=system, machine=machine, system_platform=system_platform,
                                   workshop_id=workshop_id, email_id=email_id,
                                   python_version=python_version, unique_user_id=unique_user_id)
    else:  # Update anyway
        user_info.distribution_name = distribution_name
        user_info.distribution_version = distribution_version
        user_info.system_version = system_version
        user_info.system = system
        user_info.machine = machine
        user_info.system_platform = system_platform

        # email_id and workshop_id are updated only when these fields are not None in the request.
        # As otherwise None will be overwritten to previously added workshop_id and email_id in case of
        # second attempt.
        if email_id is not None:
            user_info.email_id = email_id
        if workshop_id is not None:
            user_info.workshop_id = workshop_id
        user_info.python_version = python_version
        user_info.unique_user_id = unique_user_id

    # Add the objects list created above to user_info and attempt objects
    # to reference the foreign key for both.
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

    # Return the key and message, whether a new unique_user_id was created
    # or previous unique_user_id was used.
    summary['message'] = message
    response = {'key': unique_user_id, 'summary': summary}
    return make_response(jsonify(response))


@application.route('/')
def default():
    return render_template('landing_page.html', response=None)


@application.route('/view/')
def data_view():
    """
    This endpoint returns the data for all the worlshops.
    """

    all_attempts = request.args.get('all_attempts')
    if all_attempts:
        all_attempts = int(all_attempts)
    # Select the operating system name and the count of its user using group_by 'UserSystemInfo.system'
    user_info = db.session.query(UserSystemInfo.system,
                                 db.func.count().label("count")).group_by(UserSystemInfo.system).all()
    os_users = {}
    for user in user_info:
        os_users[user.system] = user.count

    # if all attempts toggle is on, select all failed install for each attempt.
    if all_attempts:
        failed_info = db.session.query(FailedInstalls.name, FailedInstalls.version,
                                       db.func.count().label("count")).group_by(FailedInstalls.name,
                                                                                FailedInstalls.version).all()
        failed_info_names = db.session.query(FailedInstalls.name,
                                             db.func.count().label("count")).group_by(FailedInstalls.name).all()
    else:
        # select all the latest attempt_ids per unique user from attempts table
        attempts = db.session.query(db.func.max(Attempts.id)).group_by(Attempts.unique_user_id).all()
        latest_attempt_ids = [x[0] for x in attempts]

        # query failed_installs table with a filter : attempt_id in latest_attempt_ids.
        failed_info = db.session.query(
            FailedInstalls.name, FailedInstalls.version,
            db.func.count().label("count")).filter(
            FailedInstalls.attempt_id.in_(latest_attempt_ids)).group_by(
            FailedInstalls.name, FailedInstalls.version).all()

        failed_info_names = db.session.query(FailedInstalls.name, db.func.count().label("count")).filter(
            FailedInstalls.attempt_id.in_(latest_attempt_ids)).group_by(FailedInstalls.name).all()

    most_failed_packages = [
        {"name": fail.name, "version": fail.version, "count": fail.count}
        for fail in failed_info
    ]

    most_failed_package_names = [
        {"name": fail.name, "count": fail.count}
        for fail in failed_info_names
    ]

    most_failed_packages = sorted(most_failed_packages, key=lambda k: k['count'], reverse=True)
    most_failed_package_names = sorted(most_failed_package_names, key=lambda k: k['count'], reverse=True)
    os_users = sorted(os_users.items(), key=operator.itemgetter(1), reverse=True)

    user_info = db.session.query(UserSystemInfo.workshop_id.distinct().label("workshop_id")).all()
    workshops = [
        user.workshop_id for user in user_info
        if user.workshop_id is not None
    ]

    response = {
        "most_failed_packages": most_failed_packages,
        "most_failed_package_names": most_failed_package_names,
        "os_users": os_users,
        "workshops": workshops,
        "workshop_id": "All workshops",
        "all_workshops": True,
        "all_attempts": all_attempts
    }

    if request.args.get('export') == 'json':
        return make_response(jsonify(response))

    return render_template('index.html', response=response)


@application.route('/view/<workshop_id>/')
def data_view_by_workshop(workshop_id):
    """
    This endpoint returns the data for a specific workshop.
    """

    all_attempts = request.args.get('all_attempts')
    if all_attempts:
        all_attempts = int(all_attempts)
    # If All workshops is selected as an option, redirect to '/view/'
    if workshop_id == "All workshops":
        return redirect(url_for('data_view'))
    user_info = db.session.query(
        UserSystemInfo.system, db.func.count().label("count")).filter_by(
        workshop_id=workshop_id).group_by(UserSystemInfo.system).all()
    os_users = {}
    for user in user_info:
        os_users[user.system] = user.count

    # if all attempts toggle is on, select all failed install for each attempt.
    if all_attempts:
        failed_info = db.session.query(
            UserSystemInfo, FailedInstalls).add_columns(
            FailedInstalls.name, FailedInstalls.version, db.func.count().label("count")).filter(
            UserSystemInfo.id == FailedInstalls.user_id,
            UserSystemInfo.workshop_id == workshop_id).group_by(
            FailedInstalls.name, FailedInstalls.version)

        failed_info_names = db.session.query(
            UserSystemInfo, FailedInstalls).add_columns(
            FailedInstalls.name, db.func.count().label("count")).filter(
            UserSystemInfo.id == FailedInstalls.user_id,
            UserSystemInfo.workshop_id == workshop_id).group_by(FailedInstalls.name)
    else:
        # select all the latest attempt_ids per unique user from attempts table
        attempts = db.session.query(
            UserSystemInfo, Attempts).add_columns(
            db.func.max(Attempts.id).label("attempt_id")).filter(
            UserSystemInfo.unique_user_id == Attempts.unique_user_id,
            UserSystemInfo.workshop_id == workshop_id
        ).group_by(Attempts.unique_user_id)
        latest_attempt_ids = [x.attempt_id for x in attempts]

        # query failed_installs table with a filter : attempt_id in latest_attempt_ids.
        failed_info = db.session.query(
            FailedInstalls.name, FailedInstalls.version, db.func.count().label("count")).filter(
            FailedInstalls.attempt_id.in_(latest_attempt_ids)).group_by(
            FailedInstalls.name, FailedInstalls.version).all()

        failed_info_names = db.session.query(FailedInstalls.name, db.func.count().label("count")).filter(
            FailedInstalls.attempt_id.in_(latest_attempt_ids)).group_by(FailedInstalls.name).all()

    most_failed_packages = [
        {"name": fail.name, "version": fail.version, "count": fail.count}
        for fail in failed_info
    ]

    most_failed_package_names = [
        {"name": fail.name, "count": fail.count}
        for fail in failed_info_names
    ]

    most_failed_packages = sorted(most_failed_packages, key=lambda k: k['count'], reverse=True)
    most_failed_package_names = sorted(most_failed_package_names, key=lambda k: k['count'], reverse=True)
    os_users = sorted(os_users.items(), key=operator.itemgetter(1), reverse=True)

    # Get a list of all the workshops
    user_info = db.session.query(UserSystemInfo.workshop_id.distinct().label("workshop_id")).all()
    workshops = [
        user.workshop_id for user in user_info
        if user.workshop_id is not None
    ]

    response = {
        "most_failed_packages": most_failed_packages,
        "most_failed_package_names": most_failed_package_names,
        "os_users": os_users,
        "workshops": workshops,
        "all_workshops": False,
        "workshop_id": workshop_id,
        "all_attempts": all_attempts
    }

    if request.args.get('export') == 'json':
        return make_response(jsonify(response))

    return render_template('index.html', response=response)


@application.route('/view/detail/')
def data_view_detail_package():
    """
    This endpoint returns the details of the selected package(s). It returns the result
    in json as well with 'export=json' as url parameter. Results are viewed in the
    form of plots and tables on details.html
    """

    package_one_name = request.args.get('package_one_name')
    package_one_version = request.args.get('package_one_version')
    package_two_name = request.args.get('package_two_name')
    package_two_version = request.args.get('package_two_version')
    if package_one_name is None:
        return redirect(url_for('data_view'))
    if package_two_name and package_two_name == package_one_name and package_one_version == package_two_version:
        package_two_name = None
    if package_one_version == "All":  # if all versions is selected, turn the version selected to None
        package_one_version = None
    if package_two_name and package_two_name == "None":
        package_two_name = None
    if package_two_version and package_two_version == "All":
        package_two_version = None

    workshop_id = request.args.get('workshop_id')
    all_attempts = request.args.get('all_attempts')
    if all_attempts:
        all_attempts = int(all_attempts)
    failed_packages = [
        {
            "package_name": package_one_name,
            "version": package_one_version,
        },
        {
            "package_name": package_two_name,
            "version": package_two_version,
        }
    ]
    response = []
    for failed_package in failed_packages:  # iterate over the loop of 2 packages
        if not failed_package['package_name']:  # in case only 1 package is selected
            continue
        if all_attempts:
            if workshop_id:
                if not failed_package['version']:
                    user_info = db.session.query(FailedInstalls, UserSystemInfo).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        UserSystemInfo.workshop_id == workshop_id
                    )
                else:
                    user_info = db.session.query(FailedInstalls, UserSystemInfo).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        FailedInstalls.name == failed_package['version'],
                        UserSystemInfo.workshop_id == workshop_id
                    )
            else:
                if not failed_package['version']:
                    user_info = db.session.query(UserSystemInfo, FailedInstalls).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                    )
                else:
                    user_info = db.session.query(UserSystemInfo, FailedInstalls).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        FailedInstalls.version == failed_package['version']
                    )

        else:
            if workshop_id:
                attempts = db.session.query(UserSystemInfo, Attempts).add_columns(
                    db.func.max(Attempts.id).label("attempt_id")).filter(
                    UserSystemInfo.unique_user_id == Attempts.unique_user_id,
                    UserSystemInfo.workshop_id == workshop_id
                ).group_by(Attempts.unique_user_id)

                latest_attempt_ids = [x.attempt_id for x in attempts]

                if not failed_package['version']:
                    user_info = db.session.query(FailedInstalls, UserSystemInfo.id).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        FailedInstalls.attempt_id.in_(latest_attempt_ids),
                        UserSystemInfo.workshop_id == workshop_id
                    )
                else:
                    user_info = db.session.query(FailedInstalls, UserSystemInfo.id).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        FailedInstalls.version == failed_package['version'],
                        FailedInstalls.attempt_id.in_(latest_attempt_ids),
                        UserSystemInfo.workshop_id == workshop_id
                    )

            else:

                attempts = db.session.query(db.func.max(Attempts.id)).group_by(Attempts.unique_user_id).all()
                latest_attempt_ids = [x[0] for x in attempts]
                if not failed_package['version']:
                    user_info = db.session.query(FailedInstalls, UserSystemInfo.id).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        FailedInstalls.attempt_id.in_(latest_attempt_ids)
                    )
                else:
                    user_info = db.session.query(FailedInstalls, UserSystemInfo.id).add_columns(
                        UserSystemInfo.distribution_name, UserSystemInfo.distribution_version,
                        UserSystemInfo.system, UserSystemInfo.system_platform,
                        UserSystemInfo.system_version, UserSystemInfo.machine,
                        UserSystemInfo.python_version, FailedInstalls.create_time).filter(
                        UserSystemInfo.id == FailedInstalls.user_id,
                        FailedInstalls.name == failed_package['package_name'],
                        FailedInstalls.version == failed_package['version'],
                        FailedInstalls.attempt_id.in_(latest_attempt_ids)
                    )

        distribution_name = []
        distribution_version = []
        system = []
        system_platform = []
        system_version = []
        machine = []
        python_version = []
        distribution_name_version = []
        create_time = []
        for user in user_info:
            distribution_name.append(user.distribution_name)
            distribution_version.append(user.distribution_version)
            if user.distribution_version and user.distribution_name:
                distribution_name_version.append(user.distribution_name + " " + user.distribution_version)
            system.append(user.system)
            system_platform.append(user.system_platform)
            system_version.append(user.system_version)
            machine.append(user.machine)
            python_version.append(user.python_version)
            fail_date_time = user.create_time
            create_time.append(str(datetime.datetime.date(fail_date_time)))

        # Delete all None from the lists and count the frequency of each entity using Counter.
        # This create a dictionary with key as entity and count as its value.
        distribution_name = Counter(filter(None, distribution_name))
        distribution_version = Counter(filter(None, distribution_version))
        distribution_name_version = Counter(filter(None, distribution_name_version))
        system = Counter(filter(None, system))
        system_platform = Counter(filter(None, system_platform))
        system_version = Counter(filter(None, system_version))
        machine = Counter(filter(None, machine))
        python_version = Counter(filter(None, python_version))
        create_time = Counter(filter(None, create_time))

        #  Sort the dictionaries on counts of each key. This converts them to lists.
        python_version = sorted(python_version.items(), key=operator.itemgetter(1), reverse=True)
        system = sorted(system.items(), key=operator.itemgetter(1), reverse=True)
        distribution_name_version = sorted(distribution_name_version.items(), key=operator.itemgetter(1), reverse=True)
        system_platform = sorted(system_platform.items(), key=operator.itemgetter(1), reverse=True)
        system_version = sorted(system_version.items(), key=operator.itemgetter(1), reverse=True)
        machine = sorted(machine.items(), key=operator.itemgetter(1), reverse=True)
        if not failed_package['version']:
            failed_package['version'] = ""
        resp = {
            "package_name": failed_package['package_name'],
            "package_version": failed_package['version'],
            "user_system_info": {
                "distribution_name": distribution_name,
                "distribution_version": distribution_version,
                "distribution_name_version": distribution_name_version,
                "system": system,
                "system_version": system_version,
                "system_platform": system_platform,
                "machine": machine,
                "python_version": python_version
            },
            "create_time": create_time,
            "workshop_id": workshop_id,
            "all_attempts": all_attempts,
        }
        response.append(resp)

    if request.args.get('export') == 'json':
        return make_response(json.dumps(response))

    return render_template('details.html', response=response)


@application.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response
