from tornado import escape
import json
import unittest
from pythonista import app, db
from flask import request

class TestCase(unittest.TestCase):

    numa = {
        "id": 1,
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

    numa_job = {
        "title": "striker",
        "tags": "arsenal, fuck giroud",
        "description": "Play ball",
        "salary_range": "12000 - 23000 ",
        "contract_type": "full-time",
        "company_id": 1
    }

    numa_job2 = {
        "title": "Defender",
        "tags": "arsenal, fuck koscielny",
        "description": "Stop scoring own goals",
        "salary_range": "98000 - 123000 ",
        "contract_type": "full-time",
        "company_id": 1
    }

    numa_missing_fields = {"name": numa['name'], "bio": numa['bio']}
    numa_updated_profile = {"name": "braaaah"}
    numa_job_missing_fields = {"title": "striker", "salary_range": "23400 - 39400"}
    login_creds = {"email": numa['email'], "password": numa['password']}
    login_wrongpw = {"email": numa['email'], "password": "kehwleq"}
    login_wrong_user = {"email": "dskjdksjdksjds", "password": "kehwleq"}

    def setUp(self):
        app.config.from_object('pythonista.config.TestingConfig')
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

    def put(self, endpoint, payload):
        response = self.app.put(endpoint, data=json.dumps(payload), content_type="application/json", \
                                follow_redirects=True)
        return response
    # ========= Test methods ======== #

    def test_get_index_works(self):
        response = self.app.get('/', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("please log in", str(response.data))

    def test_get_index_with_session(self):
        signup      = self.post('/api/companies', self.numa)
        login       = self.post('/login', self.login_creds)
        response    = self.app.get('/')
        with self.app.session_transaction() as session:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.numa['email'], session['company'])

    def test_get_register_works(self):
        response = self.app.get('/api/companies', content_type="text/html")
        self.assertEqual(response.status_code, 200)


    def test_post_register_works(self):
        response        = self.post('/api/companies', self.numa)
        json_response   = self.decode_json(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', json_response)
        self.assertIn('/api/companies/1',response.headers['Location'])

    def test_register_missing_fields(self):
        response        = self.post('/api/companies', self.numa_missing_fields)
        server_response = self.decode_json(response.data)
        self.assertIn("Incomplete request, Missing required fields.", server_response['error'])

        self.assertEqual(server_response['status_code'], 409)

    def test_register_username_taken(self):
        response_one    = self.post('/api/companies', self.numa)
        response_two    = self.post('/api/companies', self.numa)
        server_response = self.decode_json(response_two.data)
        self.assertIn("A company is already registered using this email", server_response['error'])
        self.assertEqual(server_response['status_code'], 409)

    def test_login_page_loads(self):
        response = self.app.get('/login', content_type="text/html")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"please submit your credentials to log in", response.data)

    def test_login_errthang_fine(self):
        signup          = self.post('/api/companies', self.numa)
        login_response  = self.post('/login', self.login_creds)

        with self.app.session_transaction() as sess:
            self.assertEqual(self.numa['email'], sess['company'])
            self.assertIn("please log in", str(login_response.data))

    def test_login_incorrect_password(self):
        signup              = self.post('/api/companies', self.numa)
        login_response      = self.post('/login', self.login_wrongpw)
        json_login_response = self.decode_json(login_response.data)
        self.assertEqual(login_response.status_code, 401)
        self.assertEqual(401, json_login_response['status_code'])
        self.assertIn("The password you provided is incorrect", json_login_response['error'])

    def test_login_incorrect_username(self):
        signup          = self.post('/api/companies', self.numa)
        login_response  = self.post('/login', self.login_wrong_user)
        json_response   = self.decode_json(login_response.data)
        self.assertEqual(login_response.status_code, 401)
        self.assertEqual(json_response['status_code'], 401)
        self.assertIn("No company is registered using this email address", json_response['error'])

    def test_logout(self):
        signup          = self.post('/api/companies', self.numa)
        login           = self.post('/login', self.login_creds)
        logout          = self.app.get('/logout', follow_redirects=True)
        with self.app.session_transaction() as session:
            self.assertNotIn('company', session)
            self.assertIn("please log in", str(logout.data))

    def test_get_companies(self):
        companies = self.app.get('/api/companies')
        json_response = self.decode_json(companies.data)
        self.assertIn('companies', json_response)
        self.assertEqual(200, companies.status_code)

    def test_get_company(self):
        signup = self.post('/api/companies', self.numa)
        company = self.app.get(signup.headers['location'])
        json_response = self.decode_json(company.data)
        self.assertIn('company', json_response)
        self.assertTrue(200, company.status_code)

    def test_publish_job_forbidden(self):
        signup = self.post('/api/companies', self.numa)
        post_job = self.post('/api/jobs', self.numa_job)
        self.assertEqual(403, post_job.status_code)
        self.assertIn('/login', post_job.headers['Location'])

    def test_publish_job_logged_in(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        self.assertTrue(201, post_job.status_code)
        self.assertIn('/api/jobs/1', post_job.headers['Location'])


    def test_publish_job_missing_fields(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job_missing_fields)
        post_job_response = self.decode_json(post_job.data)
        self.assertEqual(409, post_job.status_code)
        self.assertEqual("Incomplete request, Missing required fields.",post_job_response['error'])

    def test_get_all_jobs(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        post_job2 = self.post('/api/jobs', self.numa_job)
        jobs = self.app.get('/api/jobs')
        self.assertEqual(200, jobs.status_code)
        self.assertIn('jobs', self.decode_json(jobs.data))

    def test_get_job(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        job = self.app.get(post_job.headers['Location'])
        self.assertEqual(200, job.status_code)

    def test_get_company_jobs(self):
        signup = self.post('/api/companies', self.numa)
        company = self.app.get(signup.headers['Location'])
        company_json = self.decode_json(company.data)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        post_job2 = self.post('/api/jobs', self.numa_job)
        company_jobs_url = company_json['company']['jobs_url']
        company_jobs_list = self.app.get(company_jobs_url)
        company_list_json = self.decode_json(company_jobs_list.data)
        self.assertTrue(200, company_jobs_list.status_code)
        self.assertIn('jobs', company_list_json)

    def test_get_job_correct_contract_type(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        get_jobs_type = self.app.get('/api/jobs/full-time')
        self.assertEqual(200, get_jobs_type.status_code)

    def test_get_jobs_invalid_contract_type(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        get_jobs_type = self.app.get('/api/jobs/solidsnakebitch')
        get_jobs_type_response = self.decode_json(get_jobs_type.data)
        self.assertEqual(404, get_jobs_type.status_code)
        self.assertEqual("Invalid contract type", get_jobs_type_response['error'])

    def test_update_job(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        job_id_url = post_job.headers['Location']
        update_job = self.put(job_id_url, self.numa_job2)
        self.assertEqual(200, update_job.status_code)
        self.assertIn("job", self.decode_json(update_job.data))

    def test_update_job_forbidden(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job = self.post('/api/jobs', self.numa_job)
        job_url = post_job.headers['Location']
        with self.app.session_transaction() as session:
            session.clear()
        update_job = self.put(job_url, self.numa_job2)
        self.assertEqual(403, update_job.status_code)
        self.assertEqual("Forbidden", self.decode_json(update_job.data)['error'])

    def test_delete_job(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job  = self.post('/api/jobs', self.numa_job)
        job_url = post_job.headers['Location']
        post_job2  = self.post('/api/jobs', self.numa_job2)
        delete_job = self.app.delete(job_url)
        delete_job_json = self.decode_json(delete_job.data)
        self.assertEqual(200, delete_job.status_code)
        self.assertIn("Job deleted", delete_job_json['message'])

    def test_delete_job_forbidden(self):
        signup = self.post('/api/companies', self.numa)
        login  = self.post('/login', self.login_creds)
        post_job  = self.post('/api/jobs', self.numa_job)
        job_url = post_job.headers['Location']
        with self.app.session_transaction() as session:
            session.clear()
        delete_job = self.app.delete(job_url)
        self.assertEqual(403, delete_job.status_code)
        self.assertEqual("Forbidden", self.decode_json(delete_job.data)['error'])

    def test_update_company_profile(self):
        signup = self.post('/api/companies', self.numa)
        company_url = signup.headers['Location']
        login  = self.post('/login', self.login_creds)
        update_profile = self.put(company_url, self.numa_updated_profile)
        update_profile_json = self.decode_json(update_profile.data)
        self.assertEqual(200, update_profile.status_code)
        self.assertIn('updated sucessfully', update_profile_json['message'])

    def test_update_company_forbidden(self):
        signup = self.post('/api/companies', self.numa)
        company_url = signup.headers['Location']
        login  = self.post('/login', self.login_creds)
        with self.app.session_transaction() as session:
            session.clear()
        update_profile = self.put(company_url, self.numa_updated_profile)
        update_profile_json = self.decode_json(update_profile.data)
        self.assertEqual(403, update_profile.status_code)
        self.assertIn('Forbidden', update_profile_json['error'])

if __name__ == "__main__":
    unittest.main()
