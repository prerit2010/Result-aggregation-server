import os,json
import unittest, uuid
from app import application, db
from app.models import UserSystemInfo, SuccessfulInstalls, FailedInstalls, Attempts

class TestCase(unittest.TestCase):
    def setUp(self):
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/result_aggregation_test.db' 
        self.application = application.test_client()
        db.create_all()

    def create_user_info(self):
        data = {
            "distribution_name": "Ubuntu", 
            "distribution_version": "15.10",
            "system_verson": "#42-Ubuntu SMP Thu May 12 22:05:35 UTC 2016",
            "system": "Linux",
            "machine": "x86_64",
            "system_platform": "Linux-4.2.0-36-generic-x86_64-with-Ubuntu-15.10-wily",
            "python_version" : "2.7.10"
            }
        return data

    def create_failed_installs(self):
        data = [
            {   "name" : "EasyMercurial",
                "version": "2.5.0",
                "error_description": "errors finding EasyMercurial version"
            },
            {   "name" : "Nose (nosetests)",
                "version": "4.0",
                "error_description": "errors finding Nose (nosetests) version"
            }
        ]
        return data

    def create_successful_installs(self):
        data = [
            {"name": "git", "version" : "2.5.0"},
            {"name": "make", "version" : "4.0"}
        ]
        return data

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_User_Info(self):
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
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : self.create_failed_installs(),
                "successful_installs": self.create_successful_installs()
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_delete_User(self):
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : self.create_failed_installs(),
                "successful_installs": self.create_successful_installs()
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        count = FailedInstalls.query.count()
        self.assertEqual(count, 2)
        user = UserSystemInfo.query.get(1)
        db.session.delete(user)
        db.session.commit()
        count = UserSystemInfo.query.count() #Count User rows
        self.assertEqual(count, 0)
        count = FailedInstalls.query.count() #Count Failure rows
        self.assertEqual(count, 0)
        count = SuccessfulInstalls.query.count() #Count Success rows
        self.assertEqual(count, 0)

    def test_post_empty_failure(self):
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": self.create_successful_installs()
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_empty_success(self):
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : self.create_failed_installs(),
                "successful_installs": []
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_empty_user_data(self):
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : self.create_failed_installs(),
                "successful_installs": self.create_successful_installs()
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_post_modifies_unique_id(self):
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": [],
                "unique_user_id" : "7dd03934-bed1-443e-a4f" #modified manually
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['summary']['message']
        self.assertEqual(message, "new id generated")

    def test_post_none_unique_id(self):
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": [],
                "unique_user_id" : None
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)['summary']['message']
        self.assertEqual(message, "new id generated")

    def test_post_with_same_unique_id(self):
        """Post the data with same unique id (same user), and count the number
           of rows of UserSystemInfo"""
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": [],
                "unique_user_id" : None
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        count = UserSystemInfo.query.count() #Count User rows
        self.assertEqual(count, 1)
        key = json.loads(response.data)['key']
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": [],
                "unique_user_id" : key #using same unique key
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        """The number of rows should remail 1 only"""
        count = UserSystemInfo.query.count() #Count User rows
        self.assertEqual(count, 1)

    def test_post_no_email_id_on_second_request(self):
        """Post the data with email id and workshop id in the first attempt.
           Now post again with the same unique id, but without email and workshop id.
        """
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": []
                }
        data['user_system_info']['email_id'] = "abc@pqr.com"
        data['user_system_info']['workshop_id'] = "XYZ"
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        key = json.loads(response.data)['key']
        user = UserSystemInfo.query.first()
        assert user.email_id is not None
        assert user.workshop_id is not None
        """POST again with same unique_user_id, but without email id and workshop_id.
           email_id and worskhop_id should not be rewritten to None"""
        
        data = {"user_system_info" : self.create_user_info(),
                "failed_installs" : [],
                "successful_installs": [],
                "unique_user_id" : key
                }
        response = self.application.post('/installation_data/', data=json.dumps(data),
                                    headers={'Content-Type':'application/json'})
        self.assertEqual(response.status_code, 200)
        user = UserSystemInfo.query.first()
        assert user.email_id is not None
        assert user.workshop_id is not None

if __name__ == '__main__':
    unittest.main()