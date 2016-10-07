from helpers import *
from models import *
from sqlalchemy.exc import IntegrityError
from app import db

def get_companies():
    companies = [company.serialise() for company in Company.query.all()]
    return 200, {"status_code": 200, "companies": companies}, {}

def get_company(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company is None:
        return not_found()
    return 200, {"status_code": 200, "company": company.serialise()}, {}

def get_company_jobs(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company is not None:
        jobs = [job.serialise() for job in Job.query.filter_by(company_id=company_id).all()]
        return 200, {"status_code": 200, "jobs": jobs}, {}
    else:
        return not_found()

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

def get_jobs():
    jobs = [job.serialise() for job in Job.query.all()]
    return 200, {"status_code": 200, "jobs":  jobs}, {}

def get_job(job_id):
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return not_found()
    return 200, {"status_code": 200, "job": job.serialise()}, {}

def get_job_type(contract_type):
    jobs = [job.serialise() for job in Job.query.filter_by(contract_type=contract_type).all()]
    if jobs is None:
        return not_found()
    return 200, {"status_code": 200, "contract_type": contract_type, "results": jobs}, {}

