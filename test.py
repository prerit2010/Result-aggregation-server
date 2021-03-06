import json
import unittest
import uuid
from app import application, db
from app.models import UserSystemInfo, SuccessfulInstalls, FailedInstalls, Attempts


class TestCase(unittest.TestCase):
    def setUp(self):
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/result_aggregation_test.db'
        self.application = application.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # ===================================================================================#
    # ======================== Initialization functions =================================#

    def create_user_info(self):
        data = {
            "distribution_name": "Ubuntu",
            "distribution_version": "15.10",
            "system_verson": "#42-Ubuntu SMP Thu May 12 22:05:35 UTC 2016",
            "system": "Linux",
            "machine": "x86_64",
            "system_platform": "Linux-4.2.0-36-generic-x86_64-with-Ubuntu-15.10-wily",
            "python_version": "2.7.10"
        }
        return data

    def create_failed_installs(self):
        data = [
            {
                "name": "EasyMercurial",
                "version": "2.5.0",
                "error_description": "errors finding EasyMercurial version"
            },
            {
                "name": "Nose (nosetests)",
                "version": "4.0",
                "error_description": "errors finding Nose (nosetests) version"
            }
        ]
        return data

    def create_successful_installs(self):
        data = [
            {"name": "git", "version": "2.5.0"},
            {"name": "make", "version": "4.0"}
        ]
        return data

    def create_database(self):
        """
        This functions creates a database having 2 users by posting to '/installation_data/'.
        Out of which one user has one attempt, while the other user has 2 attempts.
        """

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": self.create_failed_installs(),
            "successful_installs": self.create_successful_installs(),
            "unique_user_id": None
        }

        data['user_system_info']['workshop_id'] = "test_workshop_1"

        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        key = json.loads(response.data.decode('utf-8'))['key']

        data['unique_user_id'] = key

        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

        data['unique_user_id'] = None
        data['user_system_info']['workshop_id'] = "test_workshop_2"

        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

        count = UserSystemInfo.query.count()  # Count User rows
        self.assertEqual(count, 2)
        count = Attempts.query.count()
        self.assertEqual(count, 3)

    # ===========================================================================#
    # ========================= Unit test cases =================================#

    def test_insert_User_Info(self):
        """Add user info directly in the database"""

        unique_user_id = str(uuid.uuid4())
        u = UserSystemInfo(distribution_name="Ubuntu", distribution_version="15.10",
                           system_version="#42-Ubuntu SMP Thu May 12 22:05:35 UTC 2016",
                           system="Linux", machine="x86_64",
                           system_platform="Linux-4.2.0-36-generic-x86_64-with-Ubuntu-15.10-wily",
                           python_version="2.7.10", unique_user_id=unique_user_id)
        db.session.add(u)
        db.session.commit()
        count = UserSystemInfo.query.count()
        self.assertEqual(count, 1)

    def test_post_data(self):
        """Post the data with all the information"""

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": self.create_failed_installs(),
            "successful_installs": self.create_successful_installs()
        }

        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_delete_User(self):
        """Create a user and the delete it"""

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": self.create_failed_installs(),
            "successful_installs": self.create_successful_installs()
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        count = FailedInstalls.query.count()
        self.assertEqual(count, 2)
        user = UserSystemInfo.query.get(1)
        db.session.delete(user)
        db.session.commit()
        count = UserSystemInfo.query.count()  # Count User rows
        self.assertEqual(count, 0)
        count = FailedInstalls.query.count()  # Count Failure rows
        self.assertEqual(count, 0)
        count = SuccessfulInstalls.query.count()  # Count Success rows
        self.assertEqual(count, 0)

    def test_post_empty_failure(self):
        """Post the data with an empty list of failed_installs"""

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": [],
            "successful_installs": self.create_successful_installs()
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_empty_success(self):
        """Post the data with an empty list of successful_installs"""

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": self.create_failed_installs(),
            "successful_installs": []
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_empty_user_data(self):
        """Post the data without any user info"""

        data = {
            "user_system_info": {},
            "failed_installs": self.create_failed_installs(),
            "successful_installs": self.create_successful_installs()
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_modifies_unique_id(self):
        """Post the data to installation_data endpoint with an accidently modified unique_user_id"""

        data = {"user_system_info": self.create_user_info(),
                "failed_installs": [],
                "successful_installs": [],
                "unique_user_id": "7dd03934-bed1-443e-a4f"  # modified manually
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data.decode('utf-8'))['summary']['message']
        self.assertEqual(message, "new id generated")

    def test_post_none_unique_id(self):
        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": [],
            "successful_installs": [],
            "unique_user_id": None
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data.decode('utf-8'))['summary']['message']
        self.assertEqual(message, "new id generated")

    def test_post_with_same_unique_id(self):
        """Post the data with same unique id (same user), and count the number
           of rows of UserSystemInfo"""

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": [],
            "successful_installs": [],
            "unique_user_id": None
        }

        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        count = UserSystemInfo.query.count()  # Count User rows
        self.assertEqual(count, 1)
        key = json.loads(response.data.decode('utf-8'))['key']
        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": [],
            "successful_installs": [],
            "unique_user_id": key  # using same unique key
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        """The number of rows should remail 1 only"""
        count = UserSystemInfo.query.count()  # Count User rows
        self.assertEqual(count, 1)

    def test_post_no_email_id_on_second_request(self):
        """Post the data with email id and workshop id in the first attempt.
           Now post again with the same unique id, but without email and workshop id.
        """

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": [],
            "successful_installs": []
        }

        data['user_system_info']['email_id'] = "abc@pqr.com"
        data['user_system_info']['workshop_id'] = "XYZ"
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        key = json.loads(response.data.decode('utf-8'))['key']
        user = UserSystemInfo.query.first()
        assert user.email_id is not None
        assert user.workshop_id is not None
        """POST again with same unique_user_id, but without email id and workshop_id.
           email_id and worskhop_id should not be rewritten to None"""

        data = {
            "user_system_info": self.create_user_info(),
            "failed_installs": [],
            "successful_installs": [],
            "unique_user_id": key
        }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                         headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        user = UserSystemInfo.query.first()
        assert user.email_id is not None
        assert user.workshop_id is not None

    def test_get_view_all(self):
        """Get request on 'view' endpoint"""

        response = self.application.get('/view/')
        self.assertEqual(response.status_code, 200)

    def test_get_workshops(self):
        """Get request on '/view/' endpoint and check the count of workshops"""

        self.create_database()
        payload = {"export": "json"}
        response = self.application.get('/view/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        workshops_count = len(response_json['workshops'])
        self.assertEqual(workshops_count, 2)

    def test_get_failed_installs_list(self):
        """Get request on '/view/' and count the failed_installs"""

        self.create_database()
        payload = {"export": "json"}
        response = self.application.get('/view/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        workshops_count = len(response_json['most_failed_packages'])
        self.assertEqual(workshops_count, 2)

    def test_get_workshops_on_workshops_page(self):
        """Get request on '/view/test_workshop_1/' endpoint and check the count of workshops"""

        self.create_database()
        payload = {"export": "json"}
        response = self.application.get('/view/test_workshop_1/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        workshops_count = len(response_json['workshops'])
        self.assertEqual(workshops_count, 2)

    def test_get_view_by_workshop(self):
        """
        Get data from '/view/test_workshop/'
        """

        unique_user_id = str(uuid.uuid4())
        u = UserSystemInfo(distribution_name="Ubuntu", distribution_version="15.10",
                           system_version="#42-Ubuntu SMP Thu May 12 22:05:35 UTC 2016",
                           system="Linux", machine="x86_64",
                           system_platform="Linux-4.2.0-36-generic-x86_64-with-Ubuntu-15.10-wily",
                           python_version="2.7.10", unique_user_id=unique_user_id, workshop_id="test_workshop")
        db.session.add(u)
        db.session.commit()
        count = UserSystemInfo.query.count()
        self.assertEqual(count, 1)
        response = self.application.get('/view/test_workshop/')
        self.assertEqual(response.status_code, 200)
        response = self.application.get('/view/test_workshop/?export=json')
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data.decode('utf-8'))
        assert 'os_users' in message
        assert 'most_failed_packages' in message

    def test_get_view_all_attempts(self):
        """Get most_failed_packages from '/view/' for all_attempts"""

        self.create_database()
        payload = {"all_attempts": "1", "export": "json"}
        response = self.application.get('/view/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        package_failed_count = response_json['most_failed_packages'][0]['count']
        self.assertEqual(package_failed_count, 3)

    def test_get_view_latest_attempt(self):
        """Get most_failed_packages from '/view/' for latest_attempt"""

        self.create_database()
        payload = {"export": "json"}
        response = self.application.get('/view/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        package_failed_count = response_json['most_failed_packages'][0]['count']
        self.assertEqual(package_failed_count, 2)

    def test_detail_latest_attempts_all_workshops(self):
        """
        Get details of a package for latest attempt and all workshops.
        """

        self.create_database()
        payload = {"package_one_name": "EasyMercurial", "package_one_version": "2.5.0", "export": "json"}
        response = self.application.get('/view/detail/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        system_count = response_json['package_details'][0]['user_system_info']['system'][0][1]  # format : [('Linux', 3), ('windows', 2)]
        self.assertEqual(system_count, 2)

    def test_detail_all_attempts_all_workshops(self):
        """
        Get details of a package for all attempt and all workshops.
        """

        self.create_database()
        payload = {
            "package_one_name": "EasyMercurial",
            "package_one_version": "2.5.0",
            "all_attempts": "1",
            "export": "json"
        }
        response = self.application.get('/view/detail/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        system_count = response_json['package_details'][0]['user_system_info']['system'][0][1]  # format : [('Linux', 3), ('windows', 2)]
        self.assertEqual(system_count, 3)

    def test_detail_latest_attempt_one_workshop(self):
        """
        Get details of a package for latest attempt and one workshop.
        """

        self.create_database()
        payload = {
            "package_one_name": "EasyMercurial",
            "package_one_version": "2.5.0",
            "workshop_id": "test_workshop_1",
            "export": "json"
        }
        response = self.application.get('/view/detail/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        system_count = response_json['package_details'][0]['user_system_info']['system'][0][1]  # format : [('Linux', 3), ('windows', 2)]
        self.assertEqual(system_count, 1)

    def test_detail_all_attempts_one_workshop(self):
        """
        Get details of a package for all attempts and one workshop.
        """

        self.create_database()
        payload = {
            "package_one_name": "EasyMercurial",
            "package_one_version": "2.5.0",
            "workshop_id": "test_workshop_1",
            "all_attempts": "1",
            "export": "json"
        }
        response = self.application.get('/view/detail/', query_string=payload)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        system_count = response_json['package_details'][0]['user_system_info']['system'][0][1]  # format : [('Linux', 3), ('windows', 2)]
        self.assertEqual(system_count, 2)

if __name__ == '__main__':
    unittest.main()
