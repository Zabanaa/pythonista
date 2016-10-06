from helpers import *
from models import *
from sqlalchemy.exc import IntegrityError
from app import db

def get_companies():
    companies = [c.serialise() for c in Company.query.all()]
    return 200, {"status_code": 200, "companies": companies}, {}

def get_company(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company is None:
        return not_found()
    return 200, {"status_code": 200, "company": company.serialise()}, {}

def publish_job(payload):

    try:
        new_job = Job(payload)
        db.session.add(new_job)
        db.session.commit()
        return 201, {"status_code": 201, "message": "Job was successfully published"}, {"Location": new_job.get_url()}
    except IntegrityError as e:
        # get error origin
        print(e)
        return "bruv"
        # check not null constraint
        # check unique constraint

def get_job(job_id):

    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return not_found()
    return 200, {"status_code": 200, "job": job.serialise()}, {}
