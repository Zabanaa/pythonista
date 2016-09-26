# Test file
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
        data = json.dumps( dict(
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

    # test violate unique constraint on register page
    # test login errthang fine
    # test login failed
    # test logout (look into the session object maybe ?)
    # test invalid JSON

if __name__ == "__main__":
    unittest.main()
