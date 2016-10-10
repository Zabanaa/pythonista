from ..errors import get_missing_fields, incomplete_request, email_already_registered
from pythonista.models import *
from sqlalchemy.exc import IntegrityError
from pythonista import db

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

def register_company(payload):

    try:
        new_company = Company(payload)
        db.session.add(new_company)
        db.session.commit()
        return 201, {"status_code": 201, "message" : "Registration successful"},{"Location": new_company.get_url()}
    except IntegrityError as e:
        cause_of_error = str(e.__dict__['orig'])
        if "violates unique constraint" in cause_of_error:
            return email_already_registered()
        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(e.__dict__['params'])
            return incomplete_request(missing_fields=missing_fields)
        else:
            return bad_request()

def publish_job(payload):

    try:
        new_job = Job(payload)
        db.session.add(new_job)
        db.session.commit()
        return 201, {"status_code": 201, "message": "Job was successfully published"}, {"Location": new_job.get_url()}
    except IntegrityError as e:
        cause_of_error = str(e.__dict__['orig'])
        if "not-null" in cause_of_error:
            missing_fields = get_missing_fields(e.__dict__['params'])
            return incomplete_request(missing_fields=missing_fields)
        else:
            return bad_request()

def get_jobs():
    jobs = [job.serialise() for job in Job.query.all()]
    return 200, {"status_code": 200, "jobs":  jobs}, {}

def get_job(job_id):
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return not_found()
    return 200, {"status_code": 200, "job": job.serialise()}, {}

def get_job_type(contract_type):
    valid_contract_types = [contract[0] for contract in Job.CONTRACTS]

    if contract_type not in valid_contract_types:
        return 404, {"status_code": 404, "error": "Invalid contract type"}, {}
    else:
        jobs = [job.serialise() for job in Job.query.filter_by(contract_type=contract_type).all()]
        return 200, {"status_code": 200, "contract_type": contract_type, "results": jobs}, {}

