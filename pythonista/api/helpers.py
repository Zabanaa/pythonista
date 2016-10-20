import os
from ..errors import get_missing_fields, incomplete_request, email_already_registered, not_found, invalid_token
from pythonista.models import *
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeSerializer
from flask import url_for, render_template
from flask_mail import Message
from pythonista import app, db, mail

email_key = "\x18\xb2\x98\"C\x0b\xae\x98\x10\x8bQ/\x8e\xf0\xee\x95\xc8\xce2\xce\xd1\x15\'\xa7"

def get_companies():
    '''
        Returns a list of all the companies registered in the database.
    '''
    companies = [company.serialise() for company in Company.query.all()]
    return 200, {"status_code": 200, "companies": companies}, {}

def get_company(company_id):
    '''
       Takes an id as a parameter.
       Returns a company instance based on the id or a 404 not found
       if there's no match.
    '''
    company = Company.query.filter_by(id=company_id).first()
    if company is None:
        return not_found()
    return 200, {"status_code": 200, "company": company.serialise()}, {}

def update_company(company_id, payload):
    '''
        Takes an id and a JSON object (in the form of a dict)
        Fetches the corresponding company instance
        Loops through the payload dictionary and updates the instance
        Commits the changes to the DB
        And returns a 200
        If the company does not exists, the function will return a 404
    '''
    company = Company.query.filter_by(id=company_id).first()
    if company is not None:
        for key, value in payload.items():
            setattr(company, key, value)
        db.session.commit()
        return 200, {"status_code": 200, "message": "Profile updated sucessfully", "company": company.serialise()}, {}
    else:
        return not_found()

def get_company_jobs(company_id):
    '''
        Takes an id, fetches the corresponding company (or 404)
        Then returns all the jobs for that company.
    '''
    company = Company.query.filter_by(id=company_id).first()
    if company is not None:
        jobs = [job.serialise() for job in Job.query.filter_by(company_id=company_id).all()]
        return 200, {"status_code": 200, "jobs": jobs}, {}
    else:
        return not_found()

def generate_token(email):
    '''
        Takes an email address
        Will return a URLSafe token to be sent in a confirmation email
        The URLSafeSerializer function will store the email in the token
    '''
    serializer = URLSafeSerializer(email_key)
    token = serializer.dumps(email)
    return token

def confirm_email(token):
    '''
        Takes the token generated above loads it, decrypts it, and returns the email
        If the token does not match we return a 404
        If the token matches, we lookup the company by their email
        We then check if the company exists in the DB
        If they do, we check if they are confirmed, in which case we send them a message along with a
        redirection url in the location header.
        If they are not confirmed we then set the confirmed attribute to True
        update the db and send a 200 with a redirection url in the location header

    '''
    serializer = URLSafeSerializer(email_key)
    try:
        email = serializer.loads(token)
    except:
        return invalid_token()

    company = Company.query.filter_by(email=email).first()

    if company is not None:
        if company.confirmed:
            return 200, {"status_code": 200, "message": "Your account is already confirmed"}, \
                        {"Location": url_for('index')}
        else:
            company.confirmed = True
            db.session.add(company)
            db.session.commit()
            return 200, {"status_code": 200, "message": "Thank you for confirming your account. You can now log in"}, \
                        {"Location": url_for('index')}
    else:
        return not_found()

def send_email(to, subject_line, body):
    '''
        Takes a recipient email, a subject line and a body
        Send the email
    '''
    message = Message(
        sender=("Karim Cheurfi", app.config['MAIL_DEFAULT_SENDER']),
        subject=subject_line,
        recipients=[to],
        html=body
    )
    mail.send(message)

def register_company(payload):

    '''
        Takes the JSON payload from the client (in the form of a dict)
        We try to create a new Company instance by passing it the payload
        We save the instance to the db
        We generate a token, a confirmation url, a subject line. We load the html email template.
        We send the email and return a 201 along with the location of that resource in the location header

        If an exception is thrown (usually an integrity error) we deal with it accordingly
    '''

    try:
        company = Company(payload)
        company.confirmed = False
        db.session.add(company)
        db.session.commit()
        token = generate_token(company.email)
        confirm_url = url_for('api.confirm_registration', token=token, _external=True)
        email_body = render_template('api/email.html', confirm_url=confirm_url)
        subject_line = "Please confirm your account"
        #send_email(company.email, subject_line, email_body)
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

    '''
        Takes a JSON payload in the form of a dict
        We try to create a new Job instance passing it the payload
        We save it to the db and return a 201
        If an exception is thrown, we deal with it accordingly
    '''

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
    '''
        Returns a list of all the jobs saved in the DB
    '''
    jobs = [job.serialise() for job in Job.query.all()]
    return 200, {"status_code": 200, "jobs":  jobs}, {}

def get_job(job_id):
    '''
        Takes an id, returns a job based on that id
        or a 404 if there's no match
    '''
    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        return not_found()
    return 200, {"status_code": 200, "job": job.serialise()}, {}

def get_job_type(contract_type):

    '''
        Takes a string as a parameter. Looks in the db and returns all jobs corresponding to that contract_type
        if the contract_type passed in is not in the default possible options, we return a 404.
    '''

    valid_contract_types = [contract[0] for contract in Job.CONTRACTS]

    if contract_type not in valid_contract_types:
        return 404, {"status_code": 404, "error": "Invalid contract type"}, {}
    else:
        jobs = [job.serialise() for job in Job.query.filter_by(contract_type=contract_type).all()]
        return 200, {"status_code": 200, "contract_type": contract_type, "results": jobs}, {}

def update_job(job_id, payload):

    '''
        Takes an id and a JSON payload in the form of a dict.
        Check if theres is a corresponding job (using the id)
        Loops through the payload and updates the instance
        If there's no match we return a 404
    '''

    job = Job.query.filter_by(id=job_id).first()

    if job is not None:
        for key, value in payload.items():
            if key is not 'id' and key is not 'company_id':
                setattr(job, key, value)

        db.session.commit()
        return 200, {"message": "sucessfully updated", "job": job.serialise()}, {}

    else:
        return not_found()

def remove_job(job_id):

    '''
        Takes an id. Fetches the corresponding job
        If it exists, we delete it and update the DB
        Else we just return a 404 not found
    '''

    job = Job.query.filter_by(id=job_id).first()
    if job is not None:
        db.session.delete(job)
        db.session.commit()
        return 200, {"status_code": 200, "message": "Job deleted sucessfully"}, {}
    else:
        return not_found()

