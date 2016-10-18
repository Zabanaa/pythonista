from ..errors import get_missing_fields, incomplete_request, email_already_registered, not_found
from pythonista.models import *
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer
from flask import url_for, render_template
from flask_mail import Message, Mail
from pythonista import *

def get_companies():
    companies = [company.serialise() for company in Company.query.all()]
    return 200, {"status_code": 200, "companies": companies}, {}

def get_company(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company is None:
        return not_found()
    return 200, {"status_code": 200, "company": company.serialise()}, {}

def update_company(company_id, payload):
    company = Company.query.filter_by(id=company_id).first()
    if company is not None:
        for key, value in payload.items():
            setattr(company, key, value)
        db.session.commit()
        return 200, {"status_code": 200, "message": "Profile updated sucessfully", "company": company.serialise()}, {}
    else:
        return not_found()

def get_company_jobs(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company is not None:
        jobs = [job.serialise() for job in Job.query.filter_by(company_id=company_id).all()]
        return 200, {"status_code": 200, "jobs": jobs}, {}
    else:
        return not_found()

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT']
        )
    except:
        return False
    return email

def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return invalid_token() 

    company = Company.query.filter_by(email=email).first()

    if company is not None:

        if company.confirmed:
            return 200, {"status_code": 200, "message": "Account already confirmed, please login"},\
            {"Location": url_for('login')}
        else:
            company.confirmed = True
            db.session.add(company)
            db.session.commit()
            return 200, {"status_code": 200, "message": "Your account is now confirmed ! You can log in"},\
            {"Location": url_for('login')}
    else:
        return not_found()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def register_company(payload):

    try:
        company = Company(payload)
        company.confirmed = False
        db.session.add(company)
        db.session.commit()
        token = generate_confirmation_token(company.email)
        confirm_url = url_for('api.confirm_registration', token=token, _external=True)
        email_body = render_template('api/email.html', confirm_url=confirm_url)
        subject = "Please confirm your registration"
        send_email(company.email, subject, email_body)
        return 201, {"status_code": 201, "message" : "Registration successful"},{"Location": company.get_url()}

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

def update_job(job_id, payload):

    job = Job.query.filter_by(id=job_id).first()

    if job is not None:
        for key, value in payload.items():
            if key is not 'id' and key is not 'company_id':
                setattr(job, key, value)

        db.session.commit()
        return 200, {"message": "sucessfully updated", "job": job.serialise()}, {} # Returns a 200 response along with a nice message

    else:
        return not_found() # 404 bitch

def remove_job(job_id):

    job = Job.query.filter_by(id=job_id).first()
    if job is not None:
        db.session.delete(job)
        db.session.commit()
        return 200, {"status_code": 200, "message": "Job deleted sucessfully"}, {}
    else:
        return not_found()

