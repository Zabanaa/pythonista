# Test file
from tornado import escape
import json
import unittest
from app import app, db
from models import *

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

numa_login_creds = dict(email="paris@numa.com", password="numaparis")

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_index_works(self):
        response = self.app.get('/', content_type="text/html")
        self.assertEqual(response.status_code, 200)

    def test_get_register_works(self):
        response = self.app.get('/register', content_type="text/html")
        self.assertEqual(response.status_code, 200)

    def test_post_register_works(self):
        response = self.app.post('/register', data=json.dumps(numa), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    # test violate not null constraint on register page
    def test_register_missing_fields(self):
        json_data = json.dumps( dict(
                email="paris@numa.com",
                location="Paris, France",
                bio="hweoiriewjr"
            )
        )
        response = self.app.post('/register', data=json_data, content_type="application/json")
        server_response = escape.json_decode(response.data)
        self.assertIn("Incomplete request. Missing required fields", server_response['message'])
        self.assertEqual(server_response['status_code'], 409)

    # test violate unique constraint on register page
    def test_register_username_taken(self):
        response_one = self.app.post('/register', data=json.dumps(numa), content_type="application/json")
        response_two = self.app.post('/register', data=json.dumps(numa), content_type="application/json")
        server_response = escape.json_decode(response_two.data)
        self.assertIn("A company is already registered", server_response['message'])
        self.assertEqual(server_response['status_code'], 409)

    def test_login_page_loads(self):
        response = self.app.get('/login', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"Bruv you want to login ?", response.data)

    # test login errthang fine
    def test_login_errthang_fine(self):
        signup          = self.app.post('/register', data=json.dumps(numa), content_type="application/json")
        login_response  = self.app.post('/login', data=json.dumps(numa_login_creds), content_type="application/json")

        self.assertEqual(login_response.status_code, 200)
        json_login_response = escape.json_decode(login_response.data)
        self.assertIn("you are logged in", json_login_response['message'])
        self.assertEqual(json_login_response['status_code'], 200)

    # test login with wrong password
    def test_login_incorrect_password(self):
        signup          = self.app.post('/register', data=json.dumps(numa), content_type="application/json")
        login_response  = self.app.post('/login', data=json.dumps(dict(
            email="paris@numa.com",
            password="wrongpasswordbruv"
        )), content_type="application/json")

        json_login_response = escape.json_decode(login_response.data)
        self.assertEqual(login_response.status_code, 401)
        self.assertEqual(401, json_login_response['status_code'])
        self.assertIn("Sorry, the password you provided is incorrect", json_login_response['message'])
    # test login with wrong username
    # test logout (look into the session object maybe ?)
    # test invalid JSON

if __name__ == "__main__":
    unittest.main()
