from tornado import escape
import json
import unittest
from app import *
from models import *
from flask import request

class TestCase(unittest.TestCase):

    numa = {
        "email":"paris@numa.com",
        "password":"numaparis",
        "name":"Numa Paris",
        "location":"Paris, France",
        "website":"paris.numa.com",
        "twitter":"numa_paris",
        "facebook":"numaparis",
        "linkedin":"numaparis",
        "bio":"Startup hub in Paris"
    }

    numa_missing_fields = {"name": numa['name'], "bio": numa['bio']}
    login_creds = {"email": numa['email'], "password": numa['password']}
    login_wrongpw = {"email": numa['email'], "password": "kehwleq"}
    login_wrong_user = {"email": "dskjdksjdksjds", "password": "kehwleq"}

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def decode_json(self, json_payload):
        return escape.json_decode(json_payload)

    def post(self, endpoint, payload):
        response = self.app.post(endpoint, data=json.dumps(payload), content_type="application/json",\
                                 follow_redirects=True)
        return response

    # ========= Test methods ======== #

    def test_get_index_works(self):
        response = self.app.get('/', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("please login", str(response.data))

    def test_get_index_with_session(self):
        signup      = self.post('/register', self.numa)
        login       = self.post('/login', self.login_creds)
        response    = self.app.get('/')
        with self.app.session_transaction() as session:
            self.assertEqual(response.status_code, 200)
            self.assertIn("Hello %s, and welcome back home" % session['company'], str(response.data))

    def test_get_register_works(self):
        response = self.app.get('/register', content_type="text/html")
        self.assertEqual(response.status_code, 200)


    def test_post_register_works(self):
        response        = self.post('/register', self.numa)
        json_response   = self.decode_json(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('resource', json_response)

    def test_register_missing_fields(self):
        response        = self.post('/register', self.numa_missing_fields)
        server_response = self.decode_json(response.data)
        self.assertIn("Incomplete request, Missing required fields.", server_response['error'])

        self.assertEqual(server_response['status_code'], 409)

    def test_register_username_taken(self):
        response_one    = self.post('/register', self.numa)
        response_two    = self.post('/register', self.numa)
        server_response = self.decode_json(response_two.data)
        self.assertIn("A company is already registered using this email", server_response['error'])
        self.assertEqual(server_response['status_code'], 409)

    def test_login_page_loads(self):
        response = self.app.get('/login', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"please submit your credentials to log in", response.data)

    def test_login_errthang_fine(self):
        signup          = self.post('/register', self.numa)
        login_response  = self.post('/login', self.login_creds)

        with self.app.session_transaction() as sess:
            self.assertEqual(login_response.status_code, 200)
            json_login_response = self.decode_json(login_response.data)
            self.assertIn("Hello %s" % sess['company'], json_login_response['message'])

    def test_login_incorrect_password(self):
        signup              = self.post('/register', self.numa)
        login_response      = self.post('/login', self.login_wrongpw)
        json_login_response = self.decode_json(login_response.data)
        self.assertEqual(login_response.status_code, 401)
        self.assertEqual(401, json_login_response['status_code'])
        self.assertIn("The password you provided is incorrect", json_login_response['error'])

    def test_login_incorrect_username(self):
        signup          = self.post('/register', self.numa)
        login_response  = self.post('/login', self.login_wrong_user)
        json_response   = self.decode_json(login_response.data)
        self.assertEqual(login_response.status_code, 401)
        self.assertEqual(json_response['status_code'], 401)
        self.assertIn("No company is registered using this email address", json_response['error'])

    def test_logout(self):
        signup          = self.post('/register', self.numa)
        login           = self.post('/login', self.login_creds)
        logout          = self.app.get('/logout', follow_redirects=True)
        json_response   = self.decode_json(logout.data)
        with self.app.session_transaction() as session:
            self.assertNotIn('company', session)
            self.assertIn('You have been logged out', json_response['message'])

if __name__ == "__main__":
    unittest.main()
