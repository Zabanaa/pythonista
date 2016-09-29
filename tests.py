from tornado import escape
import json
import unittest
from app import app, db
from models import *

class TestCase(unittest.TestCase):

    numa = dict(
        email="paris@numa.com",
        password="numaparis",
        name="Numa Paris",
        location="Paris, France",
        website="paris.numa.com",
        twitter="numa_paris",
        facebook="numaparis",
        linkedin="numaparis",
        bio="Startup hub in Paris"
    )

    numa_missing_fields = dict(
        name="Numa Paris",
        bio="Startup hub in Paris"
    )

    numa_login_creds = dict(email="paris@numa.com", password="numaparis")

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self, json_payload):
        response = self.app.post('/register', data=json.dumps(json_payload), content_type="application/json")
        return response

    def decode_json(self, json_payload):
        return escape.json_decode(json_payload)

    # ========= Test methods ======== #

    def test_get_index_works(self):
        response = self.app.get('/', content_type="text/html")
        self.assertEqual(response.status_code, 200)

    def test_get_register_works(self):
        response = self.app.get('/register', content_type="text/html")
        self.assertEqual(response.status_code, 200)

    def test_post_register_works(self):
        response = self.register_user(self.numa)
        self.assertEqual(response.status_code, 201)

    def test_register_missing_fields(self):
        response = self.register_user(self.numa_missing_fields)
        server_response = self.decode_json(response.data)
        self.assertIn("Incomplete request. Missing required fields", server_response['message'])
        self.assertEqual(server_response['status_code'], 409)

    def test_register_username_taken(self):
        response_one = self.register_user(self.numa)
        response_two = self.register_user(self.numa)
        server_response = self.decode_json(response_two.data)
        self.assertIn("A company is already registered", server_response['message'])
        self.assertEqual(server_response['status_code'], 409)

    def test_login_page_loads(self):
        response = self.app.get('/login', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"Bruv you want to login ?", response.data)

    def test_login_errthang_fine(self):
        signup          = self.register_user(self.numa)
        login_response  = self.app.post('/login', data=json.dumps(self.numa_login_creds), content_type="application/json")
        self.assertEqual(login_response.status_code, 200)
        json_login_response = self.decode_json(login_response.data)
        self.assertIn("you are logged in", json_login_response['message'])
        self.assertEqual(json_login_response['status_code'], 200)

    def test_login_incorrect_password(self):
        signup          = self.register_user(self.numa)
        login_response  = self.app.post('/login', data=json.dumps(dict(
            email="paris@numa.com",
            password="wrongpasswordbruv"
        )), content_type="application/json")

        json_login_response = self.decode_json(login_response.data)
        self.assertEqual(login_response.status_code, 401)
        self.assertEqual(401, json_login_response['status_code'])
        self.assertIn("Sorry, the password you provided is incorrect", json_login_response['message'])
    # test login with wrong username
    # test logout (look into the session object maybe ?)
    # test invalid JSON

if __name__ == "__main__":
    unittest.main()
