# Test file
from tornado import escape
import json
import unittest
from app import app, db
from models import *

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
        response = self.app.post('/register', data=json.dumps(dict(
            email="paris@numa.com",
            password="numaparis",
            name="Numa Paris",
            location="Paris, France",
            website="paris.numa.com",
            twitter="numa_paris",
            facebook="numaparis",
            linkedin="numaparis",
            bio="Startup hub in Paris"
        )), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    # test violate not null constraint on register page
    def test_register_missing_fields(self):
        json_data = json.dumps( dict(
                email="paris@numa.com",
                location="Paris, France",
                website="paris.numa.com",
                twitter="numa_paris",
                facebook="numaparis",
                linkedin="numaparis",
                bio="hweoiriewjr"
            )
        )
        response = self.app.post('/register', data=json_data, content_type="application/json")
        server_response = escape.json_decode(response.data)
        self.assertIn("Incomplete request. Missing required fields", server_response['message'])
        self.assertEqual(server_response['status_code'], 409)

    # test violate unique constraint on register page
    def test_register_username_taken(self):
        json_data = json.dumps( dict(
                email="paris@numa.com",
                password="hehkwehwke",
                name="numa paris",
                location="Paris, France",
                website="paris.numa.com",
                twitter="numa_paris",
                facebook="numaparis",
                linkedin="numaparis",
                bio="hweoiriewjr"
            )
        )
        response_one = self.app.post('/register', data=json_data, content_type="application/json")
        response_two = self.app.post('/register', data=json_data, content_type="application/json")
        server_response = escape.json_decode(response_two.data)
        self.assertIn("A company is already registered", server_response['message'])
        self.assertEqual(server_response['status_code'], 409)

    def test_login_page_loads(self):
        response = self.app.get('/login', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"Bruv you want to login ?", response.data)

    # test login errthang fine
    # test login with wrong password
    # test login with wrong username
    # test logout (look into the session object maybe ?)
    # test invalid JSON

if __name__ == "__main__":
    unittest.main()
