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
        pass

    def test_get_register_works(self):
        pass

    def test_post_register_works(self):
        pass

    # test violate not null constraint on register page
    # test violate unique constraint on register page
    # test login errthang fine
    # test login failed
    # test logout (look into the session object maybe ?)
    # test invalid JSON

if __name__ == "__main__":
    unittest.main()
